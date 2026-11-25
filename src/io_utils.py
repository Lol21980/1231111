from pathlib import Path
import pandas as pd


def read_csv_safely(path, nrows=None):
    """Try common encodings and separators; returns pandas DataFrame."""
    errors = []
    for encoding in ('utf-8', 'utf-8-sig', 'cp1251', 'latin1'):
        for sep in (None, ',', ';', '\\t'):
            try:
                return pd.read_csv(path, encoding=encoding, sep=sep, engine='python', nrows=nrows)
            except Exception as exc:
                errors.append(str(exc))
    raise RuntimeError(f'Unable to read {path}: {errors[-1]}')


def save_formats(df, stem='source'):
    out = Path('data/interim'); out.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out / f'{stem}.parquet', compression='snappy', index=False)
    df.to_feather(out / f'{stem}.feather')
    df.to_pickle(out / f'{stem}.pkl')
