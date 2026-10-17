# Laya-first data-access audit

The first revision's historical-reference lookup parsed the labelled historical
challenge prediction file while searching for unrelated validation IDs. It did
not use expected labels, pass them to either model, train, or select thresholds
from them. Nonetheless, the lookup crossed the intended access boundary.

Before fresh revision2 benchmarking, protocol amendment2 restricts this historical
cache to challenge IDs after the operating configuration is frozen. Validation
lookups cannot open that file. Automated barrier tests cover both pre-freeze and
post-freeze validation lookups.

The57authored challenge cases were already evaluated historically and are not a
new blind benchmark. They remain frozen regression/challenge cases; no expected
answer, prompt or weight was changed to resolve a challenge failure. The blocking
aggregation amendment used only the separate80-record validation sample.

No new synthetic frozen/adversarial/OOD answer file was used for training or
routing selection. Those predictions are persisted before their protected labels
are opened for scoring. Calibration uses its separate group-isolated folds.

The original protocols, source snapshots, completed model outputs and the explicit
protocol amendment are retained. Two revision1 full-Qwen validation responses are
reused only after exact model/request identity checks. Neither response contains
or received a golden label.
