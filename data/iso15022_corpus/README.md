# ISO15022 parser corpus

This is a provenance-tracked parser fixture corpus, not a production SWIFT dataset.

| Directory | Items | Status |
|---|---:|---|
| official_examples | 1 | Short literal Clearstream illustrative disclosure-message excerpt |
| public_examples | 0 | No production messages incorporated |
| standards_derived | 1,100 | Locally authored, structurally generated PARTIAL messages |
| malformed | 500 | Deliberate mutations, some tolerated/partial rather than invalid |

`sources.jsonl` commits each item's raw and complete-file hashes plus URL, organisation,
retrieval date, message type, source type and notes. `research_sources.json` records
public documentation and licensing/access limitations. Full copyright documents are
not redistributed here. The official example's overlength SEME is preserved as unknown.

The subset parser does not implement full network/mandatory-field conformance. None
of these partial fixtures is claimed as a valid production FIN message. Unknown tags,
qualifiers, data-source schemes, unsupported alternatives and original raw text survive.

Rebuild only in a new experiment workspace using the README reproduction command, or:

```bash
.venv/bin/python -m hybrid.corpus
.venv/bin/python -m scripts.expand_iso_fixtures
.venv/bin/python -m scripts.verify_iso
```

The second step adds explicit linked notification/narrative/replacement/cancellation
chains and voting-related option codes. No fixture is semantic training data. Evaluation
of generated parser assertions is separate from model accuracy and final event accuracy.
