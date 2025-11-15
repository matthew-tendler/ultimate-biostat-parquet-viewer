import streamlit as st

from biostat.data_loader import load_parquet_file
from biostat.distributions import show_distribution_tools
from biostat.pca import render_pca_analysis
from biostat.profiling import show_basic_profile
from biostat.survival import render_survival_analysis
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

        tabs = st.tabs(
            [
                "Profiling",
                "Distributions",
                "PCA",
                "Survival",
            ]
        )

        with tabs[0]:
            show_basic_profile(df)
        with tabs[1]:
            show_distribution_tools(df)
        with tabs[2]:
            render_pca_analysis(df)
        with tabs[3]:
            render_survival_analysis(df)

if __name__ == "__main__":
    main()
