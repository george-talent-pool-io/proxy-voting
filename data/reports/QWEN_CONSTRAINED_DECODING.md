# Qwen constrained decoding experiment

Status: **FORMULATION/PREFLIGHT COMPLETE; FULL HELD-OUT BENCHMARK PENDING**.
Automation is disabled; customer accuracy is unknown. No fine-tuning decision has been made from these probes.

## Exact model, tokenizer and labels

Installed `qwen3.8:27b-q4_K_M`, Ollama digest `25b843619e944cd0ae6069f94ff4e5e26a16e109ccbc0a66a0f05979ed70098e`, official lineage `Qwen/Qwen3.8-27B` revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Apache-2.0. The constrained runtime reuses the exact installed 16,810,714,464-byte language GGUF; no second large checkpoint was downloaded.

The pinned official Qwen3_5Tokenizer and native GGUF `/tokenize` agree: **A=32 → YES, B=33 → NO, C=34 → UNKNOWN**. Votability maps these semantic values to VOTABLE/NOT_VOTABLE/UNCERTAIN. The fixed version is `qwen38-three-token-v2`; one token means the bare label, not a quoted JSON string. YES/NO/UNKNOWN themselves also tokenize to individual IDs in this tokenizer, but the neutral A/B/C mapping is fixed to avoid an assumption about labels/tokenization. Leading-space and quotation-prefixed variants have different IDs.

## Runtime and genuine score availability

The installed Ollama 0.34.3 API exposes logprobs/top_logprobs: **AVAILABLE**, contrary to assuming Ollama never supports them. However a JSON-string enum response uses three generated tokens and its first token can be a quotation-prefixed label, with no guarantee that all three alternatives are returned. It does not meet the exact-one-token/all-alternatives requirement by itself.

The controlled native arm therefore uses **llama.cpp server10210 (000547513)** on loopback11436, offline, context32,768, one slot, all supported Metal layers. It uses the official chat template with thinking disabled, GBNF `root ::= "A" | "B" | "C"`, `n_predict=1`, `n_probs=64`, `post_sampling_probs=true`, temperature1 with sampling filters removed, fixed seed42. All allowed token probabilities must actually appear and be finite; a missing alternative is a runtime failure/UNKNOWN, never an invented zero.

The selected prediction is the argmax of native allowed-token scores. The sampled emitted token is retained separately, so stochastic emission does not silently redefine the classifier. Native allowed-token mass was not exactly1 in the initial probe (approximately0.9917); normalized A/B/C values are explicitly the permitted-alternative conditional distribution, not real-world correctness confidence. Native scores, mass, normalized values, top, runner-up, margin and entropy are persisted. Numerical confidence remains null until independent correctness calibration is supported.

## Fair comparison and evidence

Normal Direct keeps its frozen common semantic prompt/schema and independent mode; constrained uses the same nine semantic definitions, input source and deterministic deadline reference. No Laya output or expected label reaches either inference call. The one-token arm changes task formulation/runtime, so any quality/latency difference is attributed to that full experimental condition, not solely to output length.

Each constrained notice needs nine document calls, then up to three source-passage candidate calls per predicate where an anchor finds relevant sentences. A retained quote must be an exact verified source substring and its passage score must match the document class. Missing evidence remains unavailable. This guarantees quotation integrity, **not independently verified semantic entailment**. Evidence calls count in latency and throughput; they are not treated as free. No blind long-document truncation is allowed; over-context material abstains.

## Measured preflight / cache findings

Generic repeated-prefix probe: approximately2.6s uncached versus0.18s for a fully repeated short prefix, with identical native probability outputs. This is a cache microbenchmark, not notice throughput.

Real TRAIN-only notice probes were materially less promising: the earlier six v1 probes had9/9,5/9,5/9,3/9,8/9,7/9 semantic-field agreement and took approximately34–68s per notice including evidence. The natural-question v2 probes on two separate TRAIN notices were6/9 and6/9, approximately41s each. These are development probes only, not held-out model quality, and remain preserved under their original formulation version.

Despite large shared source prefixes, the current hybrid recurrent-model/runtime cache often reused only234 tokens and re-evaluated roughly480 remaining tokens per predicate. Eight context checkpoints/minimum step128 did not eliminate this. The notice is **not** encoded once and freely reused for all nine questions in the current implementation. Prompt ingestion and evidence scoring dominate; one generated token alone has not demonstrated a speed advantage. Separate prompt/evaluation and generation token/timing fields remain in each raw response.

A complete end-to-end TRAIN software smoke executed both independent normal and constrained pipelines, yielding complete ten-field outputs with confidence null. One clearly separated real-model pytest smoke executes the native classifier, verifies one generated token and all three native alternative scores. These establish execution, not classifier correctness.

## Held-out quality, resources and calibration

Formal normal-vs-constrained VALIDATION/CALIBRATION/frozen/adversarial/OOD/challenge results, critical-positive recall, exact match, p50/p95 throughput, repeat stability, resource peaks, Brier/ECE and coverage/review curves are **pending** until committed artifacts exist. The benchmark runs one heavy framework at a time on the64GB Apple M3 Max Mac. Per-process RSS/system pressure are sampled; shared Apple unified memory is not summed as independent VRAM.

Correctness calibration uses only English CALIBRATION/FIT, with disjoint duplicate groups for CALIBRATION/EVALUATION. Logistic correctness calibration is fixed in advance; isotonic raw-top diagnostics are separate and are not selected on held-out outcomes. Raw token probabilities are additional features, not a substitute for calibration. No numeric correctness estimate is displayed when support or calibration quality is inadequate. Non-English/OOD/conflicting/schema-invalid outputs force review.

## Training decision and current recommendation

The constrained experiment must complete on validation before the final training-decision gate. Current TRAIN probes suggest a possible semantic-quality and latency disadvantage, so no decision to replace normal Direct is justified. Preserve both arms and measure them. Do not fine-tune merely because raw class probabilities are available.

Sources: [Ollama Chat API](https://docs.ollama.com/api/chat), [llama.cpp server API](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), [official Qwen3.8-27B model](https://huggingface.co/Qwen/Qwen3.8-27B). Retrieved2026-10-17. Exact requests/responses, tokenizer pins and software versions are in `data/experiments/qwen-domain-v1/` and local preflight artifacts.
