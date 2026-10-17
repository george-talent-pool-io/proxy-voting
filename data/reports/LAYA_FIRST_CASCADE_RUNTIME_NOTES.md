# Laya-first native runtime measurements


Measured source hash: `20561a0c67435a08371e34b42db4f2eacdc8ff717bc009cdd4230f92bca64a19`.


This note clarifies the live evaluation report: `tokens_cached` is retained state after processing, not the amount of prompt reused. Use **`timings.cache_n`** for actual reuse. The raw benchmark preserves both counters.


| Source length | Cache requested | Three predicate calls | Reused prefix tokens by call |
|---|---|---|---|

| 474 | False | 9.58s | [0, 0, 0] |

| 474 | True | 9.69s | [0, 0, 0] |

| 1191 | False | 12.22s | [0, 0, 0] |

| 1191 | True | 12.49s | [0, 0, 0] |

| 6152 | False | 28.78s | [0, 0, 0] |

| 6152 | True | 17.53s | [663, 665, 667] |


The two shorter inputs reused zero prefix tokens. The longest reused 663–667 tokens per call when enabled, reducing measured three-call time from28.78s to17.53s. This was one sequential probe, not a replicated speedup estimate.


The pinned hybrid/recurrent-model runtime can invalidate earlier cache checkpoints when the question suffix changes. A `cache_prompt=true` request does not guarantee reuse. There is no demonstrated encode-once, branch-many-predicate API in this integration.


All18calls generated one class token. Prompt ingestion dominated latency. The frozen classifier still preserves all three native alternative scores. Raw probabilities remain uncalibrated.


This postprocessing note changes no model, prompt, threshold, label or stored prediction. The separate validation/cascade experiment remains in progress.
