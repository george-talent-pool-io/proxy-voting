# Qwen 4 release verification

Verified 22 October 2026 against primary sources and Hugging Face's live API.

**No official downloadable Qwen 4 checkpoint was found. Qwen 4 evaluation is NOT RUN.**
The framework's model adapter is configurable; availability is not inferred from a Transformers architecture name or a community repository title.

| Source | Finding |
|---|---|
| [Official Qwen Hugging Face catalogue](https://huggingface.co/Qwen/models) and `api/models?author=Qwen&search=Qwen4&full=true` | Official Qwen4 search returned an empty list. Exact API response and retrieval time are archived. |
| [Alibaba, full-stack AI roadmap, 22 September 2026](https://www.alibabacloud.com/en/press-room/alibaba-unveils-roadmap-on-full-stack-ai-strategy) | Qwen 4 described as in training. |
| [Official Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | An architecture preview associated with Qwen 4, not the requested locally runnable Qwen 4 successor. Configuration says `qwen4_exp`; model card advertises 180B and the Qwen community licence. |
| [Transformers qwen4_exp documentation](https://huggingface.co/docs/transformers/v5.20.0/model_doc/qwen4_exp) | Software architecture support does not establish release of a usable checkpoint. |
| [IteraCompute/Qwen4-27B-NVFP4](https://huggingface.co/IteraCompute/Qwen4-27B-NVFP4/tree/main) | Preparation repository: README and attributes, no weights. Its description explicitly says it is not inference-ready. |
| [logic65/Whittle-Next-27B-A3B](https://huggingface.co/logic65/Whittle-Next-27B-A3B) | Community research using earlier Qwen lineage. Not an official Qwen 4 release or a suitable silent substitute. |

Machine-readable evidence: `data/experiments/reliability-programme-20261022/research/`.

The already installed, pinned `mlx-community/Qwen3.8-27B-4bit` remains a separately named reference model, based on official Qwen3.8-27B. No checkpoint is renamed Qwen 4. No additional model was downloaded. The 180B preview was not selected for this 64-GB local machine.

## Release admission rule

Before a future Qwen 4 run: require official upstream weights, immutable revision/digest, tokenizer, licence and commercially suitable deployment review, supported local runtime, load/schema/evidence tests, and a fresh population-specific calibration. Existing calibration is never transferred by model-family name. The exact checkpoint is then a new experimental condition, selected on validation before independent qualification.
