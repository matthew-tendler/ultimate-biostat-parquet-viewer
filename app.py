import streamlit as st

from biostat.data_loader import load_parquet_file
from biostat.distributions import render as render_distributions
from biostat.pca import render as render_pca
from biostat.profiling import show_basic_profile
from biostat.survival import render as render_survival
from biostat.utils import clean_missing
from ui.layout import render_sidebar, set_page_config

def main():
    set_page_config()
    render_sidebar()

    st.title("Ultimate Biostat Parquet Viewer")

    uploaded_file = st.file_uploader("Upload a Parquet file", type=["parquet"])

    if uploaded_file:
        df = load_parquet_file(uploaded_file)
        df = clean_missing(df)

        st.write("Data preview:")
        st.dataframe(df.head())

        tab_profile, tab_dist, tab_pca, tab_surv = st.tabs(
            [
                "Profiling",
                "Distributions",
                "PCA",
                "Survival",
            ]
        )

        with tab_profile:
            show_basic_profile(df)
        with tab_dist:
            render_distributions(df)
        with tab_pca:
            render_pca(df)
        with tab_surv:
            render_survival(df)

if __name__ == "__main__":
    main()
