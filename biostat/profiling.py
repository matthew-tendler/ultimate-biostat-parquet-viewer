import streamlit as st
import pandas as pd

from biostat.utils import clean_missing

def show_basic_profile(df: pd.DataFrame):
    df = clean_missing(df)

    st.write("Shape:", df.shape)

    st.write("Missing values:")
    missing = df.isna().sum().reset_index()
    missing.columns = ["variable", "missing"]
    st.dataframe(missing)

    st.write("Column types:")
    st.write(df.dtypes)
