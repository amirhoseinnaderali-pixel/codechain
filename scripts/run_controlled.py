import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

import yaml

from agents import call_model


def extract_code(text):
    text = (text or "").strip()
    fence = chr(96) * 3
    python_fence = fence + "python"
    if python_fence in text:
        return text.split(python_fence, 1)[1].split(fence, 1)[0].strip()
    if fence in text:
        parts = text.split(fence)
        if len(parts) >= 3:
            return parts[1].strip()
    return text


def run_code(code, input_data, timeout=8):
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            ["python3", "-c", code],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "passed_process": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timed_out": False,
            "seconds": time.perf_counter() - started,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "passed_process": False,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + "\nExecution timeout",
            "timed_out": True,
            "seconds": time.perf_counter() - started,
        }


def evaluate(code, tests):
    rows = []
    for test in tests:
        result = run_code(code, test["input"])
        actual = result["stdout"].strip()
        expected = str(test["expected_output"]).strip()
        rows.append(
            {
                "passed": result["passed_process"] and not result["timed_out"] and actual == expected,
                "expected": expected,
                "actual": actual,
                "stderr": result["stderr"],
                "timed_out": result["timed_out"],
            }
        )
    return {
        "passed_count": sum(r["passed"] for r in rows),
        "total": len(rows),
        "all_passed": bool(rows) and all(r["passed"] for r in rows),
        "rows": rows,
    }


def generation(prompt, model, api_key):
    started = time.perf_counter()
    result = call_model(model, prompt, api_key)
    result["generation_seconds"] = time.perf_counter() - started
    return result


def direct_candidate(task, model, api_key):
    prompt = (
        "Write a complete Python 3 program for this problem. Return only code.\n\n"
        + task["problem"]
    )
    result = generation(prompt, model, api_key)
    if not result["success"]:
        return None, result
    return extract_code(result["output"]), result


def chain_candidates(task, models, api_key):
    candidates = []
    current = None
    total_generation_seconds = 0.0

    for step, model in enumerate(models, 1):
        if step == 1:
            prompt = (
                "Write a complete Python 3 program for this problem. Return only code.\n\n"
                + task["problem"]
            )
        else:
            prompt = (
                f"Improve the previous Python program for the problem below. "
                f"Return only the complete corrected program.\n\n"
                f"Problem:\n{task['problem']}\n\n"
                f"Previous program:\n[CODE]\n{current}\n[/CODE]"
            )

        result = generation(prompt, model, api_key)
        total_generation_seconds += result["generation_seconds"]

        if not result["success"]:
            candidates.append(
                {
                    "step": step,
                    "model": model,
                    "success": False,
                    "error": result["error"],
                }
            )
            continue

        current = extract_code(result["output"])
        candidates.append(
            {
                "step": step,
                "model": model,
                "success": True,
                "code": current,
                "generation_seconds": result["generation_seconds"],
            }
        )

    return candidates, total_generation_seconds


def summarize_selection(candidates):
    successful = [c for c in candidates if c.get("success")]
    if not successful:
        return None
    return successful[-1]


def run_task(task, condition, cfg):
    api_key = os.environ["GOOGLE_API_KEY"]
    if condition == "single":
        code, raw = direct_candidate(task, cfg["model_single"], api_key)
        if code is None:
            return {"task_id": task["id"], "condition": condition, "history": [raw]}
        visible = evaluate(code, task["feedback_tests"])
        heldout = evaluate(code, task["eval_tests"])
        return {
            "task_id": task["id"],
            "condition": condition,
            "calls": 1,
            "selected_step": 1,
            "visible": visible,
            "heldout": heldout,
            "generation_seconds": raw["generation_seconds"],
        }

    candidates, total_seconds = chain_candidates(
        task, cfg["model_chain"], api_key
    )

    scored = []
    for candidate in candidates:
        if candidate.get("success"):
            candidate = dict(candidate)
            candidate["visible"] = evaluate(candidate["code"], task["feedback_tests"])
            candidate["heldout"] = evaluate(candidate["code"], task["eval_tests"])
            scored.append(candidate)

    if not scored:
        return {
            "task_id": task["id"],
            "condition": condition,
            "calls": len(cfg["model_chain"]),
            "selected_step": None,
            "candidates": candidates,
            "generation_seconds": total_seconds,
        }

    if condition == "chain_final":
        selected = scored[-1]
    else:
        selected = max(
            scored,
            key=lambda c: (c["visible"]["passed_count"], -c["step"]),
        )

    return {
        "task_id": task["id"],
        "condition": condition,
        "calls": len(cfg["model_chain"]),
        "selected_step": selected["step"],
        "visible": selected["visible"],
        "heldout": selected["heldout"],
        "generation_seconds": total_seconds,
        "candidates": [
            {
                "step": c["step"],
                "model": c["model"],
                "visible_passed": c["visible"]["passed_count"],
                "heldout_passed": c["heldout"]["passed_count"],
            }
            for c in scored
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/research.yaml")
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    tasks = json.loads(Path(cfg["tasks_file"]).read_text())["tasks"]

    output = {
        "task_hash": hashlib.sha256(
            json.dumps(tasks, sort_keys=True).encode()
        ).hexdigest()[:16],
        "model_single": cfg["model_single"],
        "model_chain": cfg["model_chain"],
        "results": [],
    }

    for condition in ["single", "chain_final", "chain_objective_select"]:
        for task in tasks:
            print(condition, task["id"])
            output["results"].append(run_task(task, condition, cfg))

    Path("results").mkdir(exist_ok=True)
    Path("results/codechain.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
