# Qwen3.8 runtime and preflight

Retrieved 2026-10-16. Sources: [official Qwen model card](https://huggingface.co/Qwen/Qwen3.8-27B), [Ollama library conversion](https://ollama.com/library/qwen3.8:27b-q4_K_M), [Ollama thinking controls](https://docs.ollama.com/capabilities/thinking).

Upstream: Qwen/Qwen3.8-27B, revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`, Apache-2.0. Official full safetensors metadata includes 27,781,427,952 parameters with vision components. Installed GGUF language-model metadata reports 27,320,697,856. The `qwen35` runtime architecture reflects its architectural lineage, not a substituted Qwen3.5 checkpoint.

Selected conversion: `qwen3.8:27b-q4_K_M`, manifest `25b843619e944cd0ae6069f94ff4e5e26a16e109ccbc0a66a0f05979ed70098e`. This is the Ollama library conversion of official Qwen weights, not a community instruction fine-tune. The 16.81 GB model plus 0.93 GB projector and metadata were downloaded once. The manifest and all five installed blobs were checked by streaming SHA-256. No additional Qwen quantisation was downloaded.

Host: Apple M3 Max, 64 GiB unified memory. Local Ollama 0.34.3 reports `thinking.values = [false, low, medium, xhigh]`, default medium. Therefore the required Thinking condition uses explicit `think="xhigh"`; `think=true` would use a different runtime default. Direct uses `think=false`. Both modes executed genuine local generation and schema validation. The output cap is 16,384 for Thinking and 2,048 for Direct, with 32,768 context. Thinking has not been shortened to match Direct latency.

An isolated local runtime listens on 127.0.0.1:11435. It reports that qwen35 does not support parallel requests in this version. All timed model comparisons therefore use one client request at a time. The two-request xhigh preflight took 568 seconds total, with native generation counts 3,180 and 2,140; its queued individual request times are not sequential benchmark latencies. It confirmed nonzero reasoning in a separate channel and valid final schema. These are preflight demonstrations, not accuracy estimates.

The pre-download unified-memory estimate was 21–28 GB including overhead; the native runtime subsequently reported about 19.48 GB model/context allocation. Additional process/system peak measurements belong to each benchmark. This is shared Apple unified memory, not discrete VRAM.

The common semantic prompt, identical schema and exact-substring verifier are shared with GLM. Qwen uses its publisher-recommended mode-specific sampling presets, pinned in LLM-CONFIGS-v3.json; GLM retains its historical temperature-zero condition. This is a supported-configuration comparison. Separate semantic quality, schema/evidence reliability, repeatability, compute and memory results determine the primary fallback after validation, not this preflight.

Reasoning text is discarded in the streaming adapter before persistence. Only its digest, character count, timings and native total-token counts are retained alongside schema-valid final answers. The runtime does not expose a separate native reasoning-token count. Invalid free-form output is likewise represented by hash/size diagnostics, not saved as reasoning prose.
