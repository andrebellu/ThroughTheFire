from __future__ import annotations

import csv


def run_benchmark():
    results = []


def save_results_csv(results, output_path: str = "benchmark_results.csv"):
    fieldnames = ["width", "height", "success", "time_sec", "plan_length", "error"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Risultati salvati in {output_path}")


if __name__ == "__main__":
    results = run_benchmark()
    save_results_csv(results)
