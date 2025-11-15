import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from .utils import clean_missing, ensure_numeric


def render(df: pd.DataFrame):
    st.header("PCA Explorer")

    df = clean_missing(df)

    numeric_cols = list(df.select_dtypes(include=["number"]).columns)

    if len(numeric_cols) < 2:
        st.warning("PCA requires at least two numeric columns.")
        return

    selected_cols = st.multiselect(
        "Select numeric columns for PCA",
        options=numeric_cols,
        default=numeric_cols[: min(5, len(numeric_cols))],
    )

    if len(selected_cols) < 2:
        st.info("Select at least two numeric variables.")
        return

    df_num = ensure_numeric(df, selected_cols)
    df_num = df_num[selected_cols].astype("float64").dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_num)

    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)

    pc_df = pd.DataFrame(
        components, columns=["PC1", "PC2"]
    )

    fig = px.scatter(pc_df, x="PC1", y="PC2")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Explained Variance")
    st.write(f"PC1: {pca.explained_variance_ratio_[0]:.2%}")
    st.write(f"PC2: {pca.explained_variance_ratio_[1]:.2%}")
