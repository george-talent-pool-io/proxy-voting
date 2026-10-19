# Local model choice after the independent workstation comparison

Decision date: 2026-10-19. Comparison repository commit: `8092c18`.
Evidence: `local-llm-lab/reports/final_model_comparison.md`,
`final_local_setup.md` and `final_comparison_data.json` in the sibling project.
No files or running services in that project were changed for this decision.

## Decision

Retain **Qwen3.8-27B** as the generative model family for this learning
framework. Keep Laya as the fast, independently calibrated specialist candidate.
There is no evidence here to replace Qwen with GLM or add a second large model
to the mandatory inference path. Run one large generative model at a time on
the development Mac.

Qwen is the best supported general workhorse in the supplied comparison, not
the winner of every domain metric. Gemma 4 31B had the highest fully useful
domain count, 9/12, at 47.23 seconds median. Optimized Qwen had 7/12 at 13.53
seconds and Gemma 4 26B-A4B had 6/12 at 7.51 seconds. Laguna did not qualify.
Those are twelve synthetic development inputs from three duplicate groups;
repeated timings are not additional independent labelled examples. Coding
results do not establish proxy-voting classification quality.

## Distinct runtime profiles

| Purpose | Exact artifact/runtime | Status in this repository |
|---|---|---|
| Frozen trainable Qwen foundation and adapter continuation on this Mac | `mlx-community/Qwen3.8-27B-4bit`, revision `10c35caafbb80f7dc6a7a432cdd11af10a6d4818`; isolated, locked MLX environment | Implemented; real optimizer/checkpoint/reload and registered inference checks recorded in the qualification evidence |
| Historical authored challenge reference | Qwen Direct through the historical pinned Ollama/GGUF condition | Preserve 92/95 supplied labelled assertions and 54/57 partial-assertion cases; no customer-accuracy interpretation |
| Optimized domain serving candidate from the sibling comparison | `qwen3.8:27b-q4_K_M`, Ollama manifest digest `25b843619e944cd0ae6069f94ff4e5e26a16e109ccbc0a66a0f05979ed70098e`; GGUF blob SHA-256 `f5f1dd8920d417aac2718b0bda3403da274301efdd6760b4f0f4b864ff2ad57d`; llama.cpp `10210 (000547513)` Metal | Recommended next serving-profile experiment; not silently substituted into a registered MLX release |

The optimized serving profile uses thinking off, 8K context, 768 output tokens,
temperature 0, seed 42, a persistent serial server, verified common-prefix reuse,
deduplicated notice input and pointer/static-schema/minified output. Its measured
13.53-second median belongs to that complete profile and short synthetic slice.
It is not the latency of this application's MLX training/inference path.
The coding profile's native thinking/32K configuration is a different task and
does not become the default voting classification prompt.

The registered trainable release deliberately retains its frozen prompt,
full semantic schema and artifact. MLX affine 4-bit weights, GGUF Q4_K_M weights
and their adapters are not interchangeable. The framework cannot claim that
an MLX-trained adapter is automatically usable by the optimized GGUF server.

## Migration gate

Before adopting the optimized serving profile, implement it as a separate local
runtime adapter with the same nine-predicate output, exact-source evidence,
deadline logic, context-overflow rejection and persisted trace. Select its
configuration using development roles, freeze it, then compare quality,
schema/evidence failures and complete-pipeline timings against the existing
profile. Fit a new, model/profile-specific calibrator; do not reuse MLX or
historical Ollama confidence artifacts.

This optional serving optimization does not replace or invalidate the completed
Laya learning study or the frozen-parent learning framework. Customer deployment
still requires qualification of the exact Linux model/runtime and independently
reviewed customer population. Automation remains disabled by default.
