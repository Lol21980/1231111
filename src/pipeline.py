import argparse, logging
from src.config import RAW, INTERIM, PROCESSED, DATASETS
from src.io_utils import read_csv_safely
from src.cleaning import clean_frame
logging.basicConfig(filename='logs/pipeline.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
def load_inputs():
    paths=[RAW/n for n in DATASETS if (RAW/n).exists()]
    if not paths: return read_csv_safely(RAW/'sample_demographics.csv')
    frames=[read_csv_safely(p) for p in paths]
    result=frames[0]
    for f in frames[1:]:
        keys=[c for c in result.columns if c in f.columns and c.lower() in ('country','country_name','year')]
        if not keys: raise ValueError('Could not find shared country/year keys')
        result=result.merge(f,on=keys,how='outer',suffixes=('','_right'))
    return result
def run(limit=None):
    df=load_inputs()
    if limit: df=df.head(limit)
    cleaned,logs=clean_frame(df)
    INTERIM.mkdir(parents=True,exist_ok=True); PROCESSED.mkdir(parents=True,exist_ok=True)
    df.to_csv(INTERIM/'source.csv',index=False)
    cleaned.to_csv(PROCESSED/'clean.csv',index=False)
    import sqlite3
    with sqlite3.connect(PROCESSED/'lab1.sqlite') as con:
        cleaned.to_sql('demographics',con,if_exists='replace',index=False)
        con.execute('CREATE INDEX IF NOT EXISTS idx_demographics_year ON demographics(year)')
    import pandas as pd
    pd.DataFrame(logs).to_csv(PROCESSED/'cleaning_log.csv',index=False)
    logging.info('Finished rows %s -> %s',len(df),len(cleaned))
    try: cleaned.to_parquet(PROCESSED/'clean.parquet',index=False)
    except ImportError: logging.warning('Parquet engine missing; install pyarrow via requirements')
    return cleaned
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--limit',type=int); run(ap.parse_args().limit)
