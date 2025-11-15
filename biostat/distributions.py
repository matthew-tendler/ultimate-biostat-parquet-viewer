import streamlit as st
import pandas as pd
import plotly.express as px
from .utils import clean_missing


def render(df: pd.DataFrame):
    st.header("Distribution Explorer")

    df = clean_missing(df)

    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    categorical_cols = list(df.select_dtypes(include=["object", "category"]).columns)

    if len(df) == 0:
        st.warning("No data available.")
        return

    col1, col2 = st.columns(2)

    with col1:
        column = st.selectbox("Variable", options=df.columns)

    with col2:
        plot_type = st.selectbox(
            "Plot Type",
            ["Histogram", "Density", "ECDF", "Boxplot", "Bar (categorical)"],
        )

    series = df[column]

    try:
        if plot_type in ["Histogram", "Density", "ECDF", "Boxplot"]:
            data = pd.to_numeric(series, errors="coerce")
        else:
            data = series

        if plot_type == "Histogram":
            fig = px.histogram(data, x=data, nbins=40)
        elif plot_type == "Density":
            fig = px.density_contour(data, x=data)
        elif plot_type == "ECDF":
            fig = px.ecdf(data, x=data)
        elif plot_type == "Boxplot":
            fig = px.box(data, y=data)
        else:
            fig = px.bar(df, x=column)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not generate plot: {e}")
