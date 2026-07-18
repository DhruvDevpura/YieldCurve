import requests
import os
import pandas as pd

"""FED GSW yield-curve loader 
THe FED's daily fitted NSS curve, 1961-present
This is the project's EXTERNAL BENCHMARK  for Phase 4 Validation

Facts:
-9 Metadata lines precede the real header -> skiprows(9)
-(-999.99) is the Fed's Sentinetal for not-applicable paramters
-BETA3 is 0.0 (Not NA) in the pre-1980 era
-SVENY Columns are continously COMPOUNDED zero-coupon yields
-File also contains SVENF/SVENPY/SVEN1F , delibarelty not loaded. Phase 2 derives forward and par independently,
the Fed's version are reserved as benchmarks
-failed downloading / missing file gives error"""

GSW_URL =  "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
PARAM_COL = ["BETA0","BETA1","BETA2","BETA3","TAU1","TAU2"]

SVENY_COL = {}
for i in range(1,31):
    SVENY_COL[f"SVENY{i:02d}"]=float(i)

def fetch_gsw(raw_dir="data/raw"):
    os.makedirs(raw_dir,exist_ok=True)

    path = f"{raw_dir}/feds200628.csv"

    if os.path.exists(path):
        return 

    response = requests.get(GSW_URL)
    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)

def load_gsw_params(raw_dir="data/raw"):
    path = f"{raw_dir}/feds200628.csv"

    df = pd.read_csv(path,skiprows=9,index_col="Date",parse_dates=True,na_values=[-999.99])

    return df[PARAM_COL]

def load_gsw_zeros(raw_dir="data/raw"):
    path = f"{raw_dir}/feds200628.csv"

    df = pd.read_csv(path,skiprows=9,index_col="Date",parse_dates=True,na_values=[-999.99])

    sv_df = df[list(SVENY_COL)]

    for val in SVENY_COL:
        sv_df = sv_df.rename(columns={val:SVENY_COL[val]})

    return sv_df