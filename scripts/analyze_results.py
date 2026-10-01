import argparse
import json
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    data = json.loads(open(args.input, encoding="utf-8").read())
    rows = []
    for result in data["results"]:
        heldout = result.get("heldout", {})
        visible = result.get("visible", {})
        rows.append(
            {
                "task_id": result["task_id"],
                "condition": result["condition"],
                "heldout_passed": heldout.get("all_passed", False),
                "heldout_pass_count": heldout.get("passed_count", 0),
                "visible_pass_count": visible.get("passed_count", 0),
                "calls": result.get("calls", 0),
                "selected_step": result.get("selected_step"),
                "generation_seconds": result.get("generation_seconds", 0.0),
            }
        )

    frame = pd.DataFrame(rows)
    summary = frame.groupby("condition").agg(
        tasks=("task_id", "count"),
        heldout_task_pass_rate=("heldout_passed", "mean"),
        heldout_test_pass_rate=("heldout_pass_count", "mean"),
        mean_visible_passed=("visible_pass_count", "mean"),
        mean_calls=("calls", "mean"),
        mean_generation_seconds=("generation_seconds", "mean"),
    )
    print(summary.to_string())
    Path = __import__("pathlib").Path
    Path("results").mkdir(exist_ok=True)
    frame.to_csv("results/task_level.csv", index=False)
    summary.to_csv("results/summary.csv")


if __name__ == "__main__":
    main()
