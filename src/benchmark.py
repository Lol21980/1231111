from pathlib import Path
import time, statistics, json
import pandas as pd
import numpy as np


def median_time(fn, repeats=3):
    fn() # warmup
    vals=[]
    for _ in range(repeats):
        t=time.perf_counter(); fn(); vals.append(time.perf_counter()-t
        )
    return statistics.median(vals)


def run():
    p=Path('data/raw/sample_demographics.csv')
    if not p.exists(): raise FileNotFoundError('Put input CSV in data/raw or use included sample')
    df=pd.read_csv(p)
    Path('data/interim').mkdir(parents=True,exist_ok=True)
    rows=[]
    for fmt,writer,reader,path in [
      ('CSV',lambda:df.to_csv('data/interim/bench.csv',index=False),lambda:pd.read_csv('data/interim/bench.csv'),'data/interim/bench.csv'),
      ('Pickle',lambda:df.to_pickle('data/interim/bench.pkl'),lambda:pd.read_pickle('data/interim/bench.pkl'),'data/interim/bench.pkl'),
      ('Feather',lambda:df.to_feather('data/interim/bench.feather'),lambda:pd.read_feather('data/interim/bench.feather'),'data/interim/bench.feather'),
      ('Parquet-snappy',lambda:df.to_parquet('data/interim/bench.parquet',compression='snappy'),lambda:pd.read_parquet('data/interim/bench.parquet'),'data/interim/bench.parquet')]:
      wt=median_time(writer); rt=median_time(reader); size=Path(path).stat().st_size/1024**2
      rows.append({'format':fmt,'size_mb':size,'write_s_median':wt,'read_s_median':rt})
    pd.DataFrame(rows).to_csv('data/processed/format_benchmark.csv',index=False)
    # category typing and groupby timing
    optimized=df.copy()
    for c in optimized.select_dtypes('object').columns:
      if optimized[c].nunique()/max(1,len(optimized))<.5: optimized[c]=optimized[c].astype('category')
    before=df.memory_usage(deep=True).sum()/1024**2; after=optimized.memory_usage(deep=True).sum()/1024**2
    catcol=next((c for c in optimized.columns if str(optimized[c].dtype)=='category'),optimized.columns[0])
    gt0=median_time(lambda:df.groupby(catcol,dropna=False).size())
    gt1=median_time(lambda:optimized.groupby(catcol,observed=True,dropna=False).size())
    pd.DataFrame([{'memory_before_mb':before,'memory_after_mb':after,'groupby_before_s':gt0,'groupby_after_s':gt1,'category_column':catcol}]).to_csv('data/processed/optimization_benchmark.csv',index=False)
    # pandas/polars measurements; use same filtered/grouped result where available
    try:
      import polars as pl
      df.to_parquet('data/interim/bench.parquet')
      pf=pl.read_parquet('data/interim/bench.parquet')
      numeric=next((c for c in pf.columns if pf[c].dtype.is_numeric()),None)
      category=next((c for c in pf.columns if pf[c].dtype==pl.String),pf.columns[0])
      operations=[]
      operations.append(('pandas_read',median_time(lambda:pd.read_parquet('data/interim/bench.parquet'))))
      operations.append(('polars_read',median_time(lambda:pl.read_parquet('data/interim/bench.parquet'))))
      operations.append(('pandas_filter',median_time(lambda:df[df[numeric].notna()] if numeric else df.copy())))
      operations.append(('polars_filter',median_time(lambda:pf.filter(pl.col(numeric).is_not_null()) if numeric else pf.clone())))
      if numeric:
        operations.append(('pandas_groupby',median_time(lambda:df.groupby(category)[numeric].median())))
        operations.append(('polars_groupby',median_time(lambda:pf.group_by(category).agg(pl.col(numeric).median()))))
        operations.append(('polars_lazy_groupby',median_time(lambda:pl.scan_parquet('data/interim/bench.parquet').group_by(category).agg(pl.col(numeric).median()).collect())))
      pd.DataFrame(operations,columns=['operation','median_seconds']).to_csv('data/processed/library_benchmark.csv',index=False)
    except ImportError: print('Install polars to run library comparison')
    print('Benchmarks written to data/processed/')

if __name__=='__main__':run()
