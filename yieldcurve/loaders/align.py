import pandas as pd

"""Calendar Alignment and data quality report
Market wide missingness ( All columns NaN) means the market was closed
Weekends are absent from source and the drop removes holiday rows

align() drops all NaN-holiday rows before intersecting 

DGS30 has no gap 2002-2006 in the dataset , the series carries values through the issuance suspension(verified against raw file)

Series specific missingness (this column NaN while others trade) means the series was absent

Sample starts from 31 July 2001 ( latest first date as it is birth of youngest series in my data report)"""

DEF_SAMPLE_START = "2001-07-31"

def data_report(df):

    trading = df.dropna(how="all")

    lines =[]
    lines.append(f"rows before drop: {len(df)} , after: {len(trading)}")

    for col in trading.columns:
        first = trading[col].first_valid_index()
        last = trading[col].last_valid_index()
        n = trading[col].count()
        lines.append(f"{col} : first date:{first} , last date:{last}, count:{n}")

        in_gap = False
        gap_start = None

        for date,value in trading.loc[first:last,col].items():

            if pd.isna(value)==True and in_gap==False:
                in_gap=True
                gap_start=date

            if pd.isna(value)==False and in_gap==True:
                in_gap=False
                lines.append(f"{col} : gap from {gap_start} until resumption on {date}")
        
    return "\n".join(lines)

def align(par,gsw,start=DEF_SAMPLE_START):
    
    par = par.loc[start:]
    gsw = gsw.loc[start:]
    par = par.dropna(how="all")

    shared = par.index.intersection(gsw.index)

    par = par.loc[shared]
    gsw = gsw.loc[shared]

    return par,gsw