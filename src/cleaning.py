import re
import pandas as pd

def normalize_columns(df):
    df=df.copy(); df.columns=[re.sub(r'[^a-z0-9_]+','_',str(c).strip().lower()).strip('_') for c in df.columns]; return df

def clean_frame(df):
    df=normalize_columns(df); initial=len(df); logs=[]
    df=df.replace(['',' ','-','—','нет данных','n/a','NA','null'],pd.NA)
    logs.append({'step':'normalize missing values','before':initial,'after':len(df),'changed_or_removed':0})
    before=len(df); df=df.drop_duplicates(); logs.append({'step':'drop exact duplicates','before':before,'after':len(df),'changed_or_removed':before-len(df)})
    for c in df.select_dtypes(include='object').columns:
        df[c]=df[c].astype('string').str.strip().replace('',pd.NA)
    for c in df.columns:
        if any(k in c for k in ('year','birth','death','fertility','population','migration','urban','marriage','age','rate','percent')):
            df[c]=pd.to_numeric(df[c],errors='coerce')
    for c in df.select_dtypes(include='number').columns:
        if df[c].notna().sum()>=4:
            q1,q3=df[c].quantile([.25,.75]); iqr=q3-q1
            df[f'{c}_outlier_iqr']=((df[c]<q1-1.5*iqr)|(df[c]>q3+1.5*iqr)).fillna(False)
    return df,logs
