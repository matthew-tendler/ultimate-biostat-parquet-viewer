import pandas as pd

def clean_missing(df):
    # Convert empty/whitespace strings to NA
    return df.replace(r"^\s*$", pd.NA, regex=True)

def ensure_numeric(df, columns):
    out = df.copy()
    for c in columns:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out
