import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA

from biostat.utils import clean_missing, ensure_numeric


def render_pca_analysis(df: pd.DataFrame) -> None:
    """Run a simple PCA workflow that handles nullable dtypes."""
    df = clean_missing(df)
    num_cols = df.select_dtypes(include=["number"]).columns

    if len(num_cols) == 0:
        st.warning("No numeric columns available for PCA.")
        return

    st.subheader("Principal Component Analysis")

    default_cols = list(num_cols)
    selected_cols = st.multiselect(
        "Columns to include in PCA",
        options=default_cols,
        default=default_cols,
    )

    if len(selected_cols) < 2:
        st.info("Select at least two numeric columns to perform PCA.")
        return

    try:
        df_numeric = ensure_numeric(df, selected_cols)
        X = df_numeric[selected_cols].astype("float64")
        X = X.dropna()
        if X.empty:
            st.warning("No complete rows remain after cleaning numeric columns.")
            return

        n_components = min(3, len(selected_cols))
        pca = PCA(n_components=n_components)
        components = pca.fit_transform(X)

        explained = pd.DataFrame(
            {
                "component": [f"PC{i+1}" for i in range(n_components)],
                "explained_variance": pca.explained_variance_ratio_,
            }
        )
        st.write("Explained variance ratio")
        st.dataframe(explained)

        comp_df = pd.DataFrame(
            components[:, :2],
            columns=["PC1", "PC2"],
        )
        comp_df["index"] = X.index
        fig = px.scatter(
            comp_df,
            x="PC1",
            y="PC2",
            hover_name="index",
            title="PCA Scatter Plot (PC1 vs PC2)",
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as exc:
        st.error(f"PCA failed: {exc}")
