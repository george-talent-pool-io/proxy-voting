# Fact-first Qwen domain corpus

`v4/` is the released 5,760-text construction. Earlier drafts are retained with rejection notices; they are not competing benchmark conditions. The data is synthetic, assistant-authored semantic atoms plus deterministic composition, not independent expert labels or thousands of individually generated frontier-model notices.

Read `v4/MANIFEST.json`, `CONSTRUCTION-QC.json`, `RELEASE-AUDIT.json` and `FROZEN-LABEL-COMMIT.json`. They record exact files, seeds, distributions, evidence spans, families, duplicate edges and limitations. Six languages are represented; native domain-language quality is not certified. Shared semantic atoms limit external validity, despite keeping generation families, minimal pairs and detected duplicates together.

* `inputs/`: source text and provenance only; no row-level facts or expected labels.
* `development/`: TRAIN and VALIDATION labels accessible through the restricted loader.
* `private/`: CALIBRATION and frozen/adversarial/OOD labels. Owner-only filesystem permissions provide an accidental-access barrier, not a cryptographic or multi-user security boundary.
* `construction-private/`: original fact-first construction ledger; never passed to inference/training loaders.

TRAIN/VALIDATION/CALIBRATION/FROZEN/ADVERSARIAL/OOD have 3,120/660/660/840/240/240 records. Calibration FIT/EVALUATION are also group-disjoint. No source text from the57-case historical challenge is a generator input; exact, lexical and local semantic checks found no configured-threshold match. Similarity checks cannot prove the absence of every semantic paraphrase.

Future changes require a new corpus version. Never edit this release in place or use frozen errors to generate training examples. The fixed57-case challenge remains a separate authored benchmark with partial labels. These data cannot establish customer accuracy or automation safety.
