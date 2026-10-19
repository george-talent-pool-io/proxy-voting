"""Real local generative fallback. No redirects, proxies, cloud endpoints or downloads."""
import hashlib
import ipaddress
import json
import os
import time
from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler
from semantic_pipeline.schema import SemanticResult, PREDICATES
from semantic_pipeline.evidence import validate_all

HERE = Path(__file__).parent

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Local inference redirects prohibited')

class SemanticFallback(Protocol):
    enabled: bool
    def analyse(self, *, original_text, narrative_text, structured_facts, laya_result=None,
                requested_predicates=PREDICATES, mode='INDEPENDENT'): ...

class DisabledFallback:
    enabled = False
    def analyse(self, **kwargs):
        return {'enabled': False, 'invoked': False, 'valid': False, 'error': 'LLM_ENABLED=false',
                'parsed': None, 'latency_ms': 0, 'evidence_validation': None}

class OllamaFallback:
    enabled = True
    def __init__(self, config=None):
        self.config = config or json.loads((HERE/'llm-config.json').read_text())
        url = urlparse(self.config['base_url'])
        # Literal loopback IP avoids DNS rebinding. Custom remote endpoints rejected.
        if url.scheme != 'http' or url.username or url.password or url.path not in ('', '/'):
            raise ValueError('Expected plain HTTP loopback runtime URL')
        try: local = ipaddress.ip_address(url.hostname).is_loopback
        except ValueError: local = False
        if not local: raise ValueError('External LLM endpoints are prohibited')
        self.opener = build_opener(ProxyHandler({}), NoRedirect())
        self.prompt = (HERE/'prompt.txt').read_text()
        self.prompt_version = digest({'prompt': self.prompt, 'schema': SemanticResult.model_json_schema()})
        self.identity = self.check_identity()

    def http(self, path, payload=None):
        req = Request(self.config['base_url'].rstrip('/')+path,
            data=json.dumps(payload, ensure_ascii=False).encode() if payload is not None else None,
            headers={'Content-Type': 'application/json'})
        with self.opener.open(req, timeout=self.config['timeout_seconds']) as response:
            return json.load(response)

    def check_identity(self):
        tags = self.http('/api/tags')['models']
        match = next((r for r in tags if r['name'] == self.config['model']), None)
        if not match or match['digest'] != self.config['model_digest']:
            raise ValueError('Installed LLM digest differs from pinned checkpoint')
        version = self.http('/api/version')['version']
        if version != self.config['runtime_version']: raise ValueError('Runtime version changed; new experiment required')
        return {'model': match, 'runtime_version': version}

    def request(self, original_text, narrative_text, structured_facts, laya_result, mode):
        if mode not in ('INDEPENDENT', 'FALLBACK'): raise ValueError('Invalid LLM mode')
        if mode == 'INDEPENDENT' and laya_result is not None:
            raise ValueError('Independent mode must not receive Laya predictions')
        context = {'mode': mode, 'original_notice': original_text, 'narrative': narrative_text,
                   'authoritative_structured_facts': structured_facts}
        if mode == 'FALLBACK':
            context.update(laya_diagnostic=laya_result,
                reason_for_escalation='SPECIALIST_GATE: semantic uncertainty or possible conflict; inspect native scores and evidence. Routing thresholds are experimental.')
        return {'model': self.config['model'], 'stream': False, 'think': self.config['think'],
            'messages': [{'role': 'system', 'content': self.prompt}, {'role': 'user',
                'content': json.dumps(context, ensure_ascii=False)}],
            'format': SemanticResult.model_json_schema(), 'keep_alive': self.config['keep_alive'],
            'options': {k: self.config[k] for k in ('temperature', 'seed', 'num_ctx', 'num_predict')}}

    def analyse(self, *, original_text, narrative_text, structured_facts, laya_result=None,
                requested_predicates=PREDICATES, mode='INDEPENDENT'):
        if not set(requested_predicates) <= set(PREDICATES): raise ValueError('Invalid requested predicates')
        request = self.request(original_text, narrative_text, structured_facts, laya_result, mode)
        result = {'enabled': True, 'invoked': False, 'mode': mode, 'model': self.config['model'],
            'model_digest': self.config['model_digest'], 'prompt_version': self.prompt_version,
            'request_hash': digest(request), 'request': request, 'parsed': None, 'raw_response': None,
            'valid': False, 'evidence_validation': None, 'confidence': None,
            'confidence_definition': 'Unavailable: no calibrated LLM probability', 'latency_ms': 0}
        # Bound total context conservatively using UTF-8 bytes (at least as many as tokens).
        # Never silently truncate; large inputs explicitly abstain for manual review.
        byte_count = sum(len(m['content'].encode()) for m in request['messages'])
        budget = self.config['num_ctx'] - self.config['num_predict'] - 256
        # ASCII typically ~4 chars/token, but only accept a strict byte upper bound.
        if byte_count > budget:
            return {**result, 'error': 'CONTEXT_BUDGET_EXCEEDED: complete input retained; no model truncation allowed'}
        start = time.perf_counter()
        try:
            self.check_identity()  # Mutable tags must match the full pin on every request.
            result['invoked'] = True
            raw = self.http('/api/chat', request)
            result['raw_response'] = raw
            if not raw.get('done') or raw.get('done_reason') != 'stop':
                raise ValueError('Incomplete model generation')
            result['parsed'] = SemanticResult.model_validate_json(raw['message']['content']).model_dump()
            result['evidence_validation'] = validate_all(original_text, result['parsed'])
            result['valid'] = True  # Invalid quotes are quarantined separately per field.
        except Exception as exc:
            result['error'] = f'{type(exc).__name__}: {exc}'
        result['latency_ms'] = (time.perf_counter()-start)*1000
        return result

def from_environment():
    return OllamaFallback() if os.environ.get('LLM_ENABLED', 'false').lower() == 'true' else DisabledFallback()
