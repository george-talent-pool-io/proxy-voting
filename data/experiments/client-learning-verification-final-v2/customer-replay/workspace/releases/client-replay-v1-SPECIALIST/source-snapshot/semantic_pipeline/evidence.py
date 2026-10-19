"""Exact source verification. Identity normalisation preserves Unicode and offsets."""
def verify_evidence(source: str, quote: str) -> dict:
    if not isinstance(source, str) or not isinstance(quote, str) or not quote or not quote.strip():
        return {'valid': False, 'normalisation': 'identity', 'reason': 'Empty or invalid quotation'}
    start = source.find(quote)
    if start < 0:
        return {'valid': False, 'normalisation': 'identity', 'reason': 'Not an exact substring'}
    return {'valid': True, 'normalisation': 'identity', 'text': quote,
            'start': start, 'end': start + len(quote)}

def validate_all(source, parsed):
    # Invalid quotations retained as diagnostics, never as displayable evidence.
    verified = {k: [verify_evidence(source, q) for q in qs] for k, qs in parsed['evidence'].items()}
    deadline = parsed['deadline_information']
    return {'predicates': verified, 'deadline': verify_evidence(source, deadline['deadline_text'])
            if deadline['deadline_text'] is not None else None,
            'invalid_count': sum(not q['valid'] for qs in verified.values() for q in qs)
                + int(deadline['deadline_text'] is not None and not verify_evidence(source, deadline['deadline_text'])['valid'])}
