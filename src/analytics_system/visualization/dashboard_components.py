import streamlit as st


def show_metrics(profile: dict):
    cols = st.columns(4)
    cols[0].metric("Rows", f"{profile.get('rows', 0):,}")
    cols[1].metric("Columns", f"{profile.get('columns', 0):,}")
    cols[2].metric("Missing cells", f"{profile.get('missing_total', 0):,}")
    cols[3].metric("Duplicate rows", f"{profile.get('duplicate_rows', 0):,}")
