#!/usr/bin/env python3
"""
Compute trigger benchmark metrics from results.json.

Input JSON format:
{
  "trials": [
    {"trial": 1, "results": [{"id":"p01","should_trigger":true,"would_trigger":true}]}
  ]
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_results(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def compute_metrics(data: dict) -> dict:
    trials = data.get("trials", [])
    if not trials:
        raise ValueError("No trials found in results data.")

    first_results = trials[0].get("results", [])
    if not first_results:
        raise ValueError("No results found in first trial.")

    ids = [item["id"] for item in first_results]
    should = {item["id"]: bool(item["should_trigger"]) for item in first_results}
    by_id: dict[str, list[float]] = {key: [] for key in ids}

    for trial in trials:
        seen = set()
        for item in trial.get("results", []):
            item_id = item["id"]
            seen.add(item_id)
            by_id[item_id].append(1.0 if item.get("would_trigger", False) else 0.0)
        missing = set(ids) - seen
        if missing:
            raise ValueError(f"Trial {trial.get('trial')} is missing ids: {sorted(missing)}")

    per_id_trigger_rate = {item_id: mean(values) for item_id, values in by_id.items()}
    per_id_agreement = {
        item_id: (1.0 if len(set(values)) == 1 else 0.0) for item_id, values in by_id.items()
    }

    positives = [item_id for item_id, flag in should.items() if flag]
    negatives = [item_id for item_id, flag in should.items() if not flag]

    recall = mean([per_id_trigger_rate[item_id] for item_id in positives])
    specificity = mean([1.0 - per_id_trigger_rate[item_id] for item_id in negatives])
    balanced_score = 0.5 * (recall + specificity)
    agreement_mean = mean(list(per_id_agreement.values()))

    return {
        "recall": recall,
        "specificity": specificity,
        "balanced_score": balanced_score,
        "agreement_mean": agreement_mean,
        "per_id_trigger_rate": per_id_trigger_rate,
        "per_id_agreement": per_id_agreement,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute trigger evaluation metrics.")
    parser.add_argument("results_json", help="Path to results.json")
    parser.add_argument(
        "--output",
        help="Output path for metrics.json. Default: same directory as results.json",
    )
    args = parser.parse_args()

    results_path = Path(args.results_json)
    output_path = Path(args.output) if args.output else results_path.with_name("metrics.json")

    data = load_results(results_path)
    metrics = compute_metrics(data)
    output_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
