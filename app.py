import streamlit as st
import numpy as np

from biostat.data_loader import load_parquet_file
from biostat.sample_data import generate_clinical_trial_data, get_sample_data_info
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

    # Data loading section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload a Parquet file", type=["parquet"])
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        load_sample = st.button("📊 Load Sample Data", type="secondary", use_container_width=True)
    
    # Load sample data if requested
    if load_sample:
        with st.spinner("Generating sample clinical trial data..."):
            df = generate_clinical_trial_data()
            st.session_state['sample_data_loaded'] = True
            st.session_state['current_df'] = df
            st.rerun()
    
    # Check if we have data from session state (sample data)
    # Prioritize uploaded file over sample data
    if uploaded_file:
        df = load_parquet_file(uploaded_file)
        df = clean_missing(df)
        # Clear sample data when user uploads their own file
        st.session_state['sample_data_loaded'] = False
        if 'current_df' in st.session_state:
            del st.session_state['current_df']
    elif 'current_df' in st.session_state:
        df = st.session_state['current_df']
        sample_loaded = st.session_state.get('sample_data_loaded', False)
    else:
        # Show info about sample data
        st.info("👋 Welcome! Upload a Parquet file or click 'Load Sample Data' to explore a simulated clinical trial dataset.")
        
        with st.expander("📖 About the Sample Dataset", expanded=False):
            info = get_sample_data_info()
            st.markdown(f"**{info['name']}**")
            st.markdown(info['description'])
            st.markdown("**Variables included:**")
            for var in info['variables']:
                st.markdown(f"- {var}")
        
        st.stop()

    # Clean missing values
    df = clean_missing(df)
    
    # Show data source indicator
    if st.session_state.get('sample_data_loaded', False):
        info = get_sample_data_info()
        st.success(f"✅ Loaded: {info['name']} ({len(df)} subjects)")
        if st.button("🔄 Load Different Sample Data"):
            with st.spinner("Generating new sample data..."):
                df = generate_clinical_trial_data(seed=np.random.randint(0, 10000))
                st.session_state['current_df'] = df
                st.rerun()

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
