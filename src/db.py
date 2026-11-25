import sqlite3
from pathlib import Path
import pandas as pd


def sqlite_load(df, db_path='data/processed/lab1.sqlite'):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        df.to_sql('demographics', con, if_exists='replace', index=False)
        con.execute('CREATE INDEX IF NOT EXISTS idx_demographics_year ON demographics(year)')
        return con


def postgres_load(df):
    """Optional PostgreSQL loader, requires DATABASE_URL and sqlalchemy/psycopg."""
    import os
    from sqlalchemy import create_engine
    url=os.getenv('DATABASE_URL')
    if not url: raise RuntimeError('Set DATABASE_URL (see .env.example)')
    engine=create_engine(url)
    df.to_sql('demographics', engine, if_exists='replace', index=False, chunksize=5000)
    return engine
