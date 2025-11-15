import pandas as pd
import plotly.express as px
import streamlit as st

from biostat.utils import clean_missing


def show_distribution_tools(df: pd.DataFrame) -> None:
    """Render histogram, density, and box plot helpers."""
    df = clean_missing(df)
    df = df.convert_dtypes()

    st.subheader("Distribution Explorer")

    if df.empty:
        st.info("No data available to profile.")
        return

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns detected for distribution plots.")
        return

    # Histogram
    hist_col = st.selectbox("Histogram column", numeric_cols, key="dist_hist_col")
    if hist_col:
        try:
            data = pd.to_numeric(df[hist_col], errors="coerce")
            clean_data = data.dropna()
            if clean_data.empty:
                raise ValueError("No numeric values remain after cleaning.")
            fig = px.histogram(
                x=clean_data,
                nbins=30,
                labels={"x": hist_col, "y": "Frequency"},
                title=f"Histogram of {hist_col}",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.warning(f"Unable to render histogram for {hist_col}: {exc}")

    # Density
    density_col = st.selectbox(
        "Density plot column", numeric_cols, key="dist_density_col"
    )
    if density_col:
        try:
            data = pd.to_numeric(df[density_col], errors="coerce")
            clean_data = data.dropna()
            if clean_data.empty:
                raise ValueError("No numeric values remain after cleaning.")
            fig = px.histogram(
                x=clean_data,
                nbins=50,
                histnorm="probability density",
                labels={"x": density_col, "y": "Density"},
                title=f"Density of {density_col}",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.warning(f"Unable to render density plot for {density_col}: {exc}")

    # Box plot
    box_col = st.selectbox("Box plot column", numeric_cols, key="dist_box_col")
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    group_options = ["(none)"] + categorical_cols
    group_col = st.selectbox(
        "Group by (optional)", group_options, key="dist_group_col"
    )

    if box_col:
        try:
            data = pd.to_numeric(df[box_col], errors="coerce")
            plot_df = pd.DataFrame({box_col: data})
            plot_df = plot_df.dropna(subset=[box_col])
            if group_col != "(none)":
                plot_df[group_col] = df.loc[plot_df.index, group_col]
            if plot_df.empty:
                raise ValueError("No numeric values remain after cleaning.")
            fig = px.box(
                plot_df,
                y=box_col,
                x=group_col if group_col != "(none)" else None,
                points="all",
                title=f"Box plot of {box_col}",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.warning(f"Unable to render box plot for {box_col}: {exc}")
