"""Post-selection fixed-ruler check, not training or model selection."""
import json
from pathlib import Path
from scripts.qualify_frozen_learning import benchmark
from training.framework import jobs, seeds
from training.framework.bundle import sha, write
from training.framework.resources import model_resource
from training.framework.whole_runtime import WholeNotice
from semantic_pipeline.metrics import summarize
root=Path("data/experiments/framework-domain-upgrade-20261022-v2")
freeze=json.loads((root/"SELECTION_FREEZE.json").read_text())
assert sha(root/"result.json")==freeze["selection_sha256"]
challenge=Path("tests/fixtures/semantic.json")
assert sha(challenge)==freeze["challenge_sha256"]
inputs=[{k:r[k] for k in ("id","text")} | {"evaluation_time":"2026-10-16T12:00:00+00:00"}
        for r in json.loads(challenge.read_text())]
conditions={"CHALLENGE_PREVIOUS":lambda:WholeNotice(jobs.member("jobs","customer-adaptation-uncontended-v1-8epoch")),
            "CHALLENGE_SELECTED":lambda:WholeNotice(freeze["seed"],model_factory=seeds.FrozenModel)}
reports={}
with model_resource("fixed-challenge-domain-candidate"):
    saved={name:benchmark(factory,inputs,root/name) for name,factory in conditions.items()}
    truth={r["id"]:r["expected"] for r in json.loads(challenge.read_text())}
    for name,predictions in saved.items():
        report=summarize([{**r,"expected":truth[r["id"]]} for r in predictions])
        write(root/name/"metrics.json",report);reports[name]=report
write(root/"CHALLENGE_RESULT.json",{"selection_unchanged":True,"challenge_sha256":sha(challenge),
    "scope":"Authored partial assertions, not customer/final-status accuracy",
    "reports":reports,"automation_enabled":False,"customer_accuracy":None})
print(json.dumps({name:{"correct_assertions":r["correct_assertions"],"assertions":r["assertions"],
    "cases_satisfying_partial_assertions":r["cases_satisfying_all_supplied_assertions"],"cases":r["cases"]}
    for name,r in reports.items()}))
