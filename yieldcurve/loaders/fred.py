import requests
import os
import pandas as pd

"""FRED CMT par-yield loader.
It fetches the 11 constant maturity treasury series ( 1MO-30Y ) from FRED and parses them into one dates x tenor matrix

Conventions and facts:
-Values are par yields in PERCENT, semi-annual bond-equivalent basis.
-Market-closed days appears as EMPTY fields in the CSV -> NaN
-NaN covers both closed days and dates before a series existed
-Columns are tenors as year fractions ( 1/12 , 1/6 , 1/2 ,...)
-Failed Download / Missing file gives error"""

DGS_SERIES = {"DGS1MO":1/12,"DGS3MO":1/4,"DGS6MO":1/2,"DGS1":1,"DGS2":2,"DGS3":3,"DGS5":5,"DGS7":7,"DGS10":10,"DGS20":20,"DGS30":30}
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

def fetch_dgs(series_ids,raw_dir = "data/raw"):
    os.makedirs(raw_dir,exist_ok=1)

    for sid in series_ids:
        path = f"{raw_dir}/{sid}.csv"

        if os.path.exists(path):
            continue

        url = FRED_CSV_URL.format(series_id =sid)

        response = requests.get(url)
        response.raise_for_status()

        with open(path, "wb") as f:
            f.write(response.content)

def load_par_yields(raw_dir="data/raw"):
    dgslist = []

    for sid in DGS_SERIES:
        path = f"{raw_dir}/{sid}.csv"
        df = pd.read_csv(path,index_col="observation_date",parse_dates=True)
        df = df.rename(columns={sid:DGS_SERIES[sid]})
        dgslist.append(df)

    combined = pd.concat(dgslist,axis=1)
    combined = combined[sorted(combined.columns)]

    return combined