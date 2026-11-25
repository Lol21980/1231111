# Results checklist

Run the scripts on the actual original datasets to produce empirical values:
- `python -m src.pipeline` -> cleaned CSV, cleaning log and SQLite DB
- `python -m src.benchmark` -> format, memory, pandas/polars timing CSV files

The benchmark figures are machine-dependent and are intentionally not fabricated in this repository. Keep machine specifications and library versions in your report.
