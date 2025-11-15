import streamlit as st
from lifelines import KaplanMeierFitter

from biostat.utils import clean_missing, ensure_numeric


def render_survival_analysis(df: pd.DataFrame) -> None:
    """Minimal Kaplan-Meier workflow with cleaning and validation."""
    df = clean_missing(df)

    if df.empty:
        st.info("No data available for survival analysis.")
        return

    st.subheader("Survival Analysis")
    columns = df.columns.tolist()
    if not columns:
        st.info("Upload data to configure survival inputs.")
        return

    time_col = st.selectbox("Time-to-event column", columns)
    event_col = st.selectbox("Event indicator column", columns, index=1 if len(columns) > 1 else 0)

    if not time_col or not event_col:
        st.info("Select both time and event columns.")
        return

    try:
        df_numeric = ensure_numeric(df, [time_col, event_col])
        time_data = df_numeric[time_col].astype("float64")
        event_data = df_numeric[event_col].astype("float64")
    except KeyError as exc:
        st.error(f"Column not found: {exc}")
        return
    except Exception as exc:
        st.error(f"Unable to prepare survival data: {exc}")
        return

    valid_mask = time_data.notna() & event_data.notna()
    if valid_mask.sum() == 0:
        st.warning("No valid time/event pairs remain after cleaning.")
        return

    try:
        kmf = KaplanMeierFitter()
        kmf.fit(time_data[valid_mask], event_observed=event_data[valid_mask])
    except Exception as exc:
        st.error(f"Survival model failed: {exc}")
        return

    survival_df = kmf.survival_function_.reset_index()
    st.line_chart(
        survival_df.set_index("timeline"),
        use_container_width=True,
    )
    st.dataframe(survival_df.head())
