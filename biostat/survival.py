import streamlit as st
import pandas as pd
from lifelines import KaplanMeierFitter
import plotly.express as px
from .utils import clean_missing, ensure_numeric


def render(df: pd.DataFrame):
    st.header("Survival Analysis")

    df = clean_missing(df)

    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    all_cols = list(df.columns)

    time_col = st.selectbox("Time column", options=all_cols)
    event_col = st.selectbox("Event column (1=event, 0=censored)", options=all_cols)

    df = ensure_numeric(df, [time_col, event_col])
    df = df[[time_col, event_col]].dropna()

    try:
        km = KaplanMeierFitter()
        km.fit(df[time_col], df[event_col])

        survival_df = pd.DataFrame({
            "timeline": km.survival_function_.index,
            "survival_prob": km.survival_function_["KM_estimate"].values,
        })

        fig = px.line(survival_df, x="timeline", y="survival_prob")
        fig.update_layout(yaxis=dict(range=[0, 1]))

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not compute KM curve: {e}")
