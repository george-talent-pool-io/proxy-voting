# Local Prowide boundary

Build once with Java11+ and Maven:

```sh
mvn -f tools/prowide/pom.xml package
.venv/bin/python -m pytest tests/unit/test_iso_adapter.py tests/integration/test_prowide.py -q
```

Core is pinned to `SRU2025-10.3.20` (Apache-2.0). `DEPENDENCIES.lock.json` records resolved transitive versions/checksums. The adapter launches the JAR lazily over local stdin/stdout, without a listening network endpoint. Downloads occur only at setup. Java objects remain inside the helper; Python receives JSON with typed components, raw source, exact spans where verified, unknown fields and provenance.

Core parsing is not complete SWIFT business/network validation. Successful status is `PARSED_NOT_VALIDATED`, never a full `VALID ISO15022` claim. A failure or sequence warning preserves source and falls back to the non-validating recovery scanner. Ordinary unstructured notices bypass Java.

`DOMAIN_ISO_ADAPTER=true` enables the adapter in the opt-in Qwen-domain application path. It is false in the frozen primary domain experiment and changes model identity when enabled. No ISO context improvement is claimed before a separate validation experiment. Historical custom-parser experiments remain reproducible.

The current Python-only Docker image does not contain Java/Maven. Host integration is verified; a Java-capable container build remains an explicit deployment task. A missing helper never silently drops a notice.

See `data/reports/ISO15022_PROWIDE_EVALUATION.md` for the full measured comparison, resource costs, source attribution and remaining limitations.
