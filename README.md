# Lab 1 — Python data processing and cleaning

Project pipeline for the course laboratory: data formats, type optimization, pandas vs polars, cleaning, SQLite and optional PostgreSQL.

> The uploaded RAR5 source archive is ~1.5 GB expanded and could not be extracted here (no RAR extraction utility in this environment). Included files are synthetic demo CSVs so the project can run immediately. Replace them with the original datasets before final empirical submission.

## Quick start (Windows)
1. Install Python 3.12.14 and Git.
2. Open this folder in VS Code.
3. In terminal: `py -3.12 -m venv .venv`
4. Activate: ` .venv\\Scripts\\Activate.ps1` (PowerShell) or ` .venv\\Scripts\\activate.bat` (cmd).
5. Install: `python -m pip install -r requirements.txt`
6. Run: `python -m src.pipeline --limit 500` for debug or `python -m src.pipeline` for full data.
7. Run benchmarks: `python -m src.benchmark`.

## Included
- `src/` reusable code for IO, cleaning, benchmarking and database loading
- `notebooks/` Jupyter notebook
- `data/raw/` synthetic sample datasets
- `sql/` SQLite/PostgreSQL DDL examples
- `docs/` report template and sample findings

## GitHub
Create an empty public repository. In this folder run:
```bash
git init
git add .
git commit -m "feat: add data cleaning pipeline for lab 1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Do not upload `.venv`, real credentials, or the large source data archive.
