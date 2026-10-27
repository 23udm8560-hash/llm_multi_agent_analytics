import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st
import pandas as pd
from analytics_system.pipelines.ingestion_pipeline import ingest_uploaded_file
from analytics_system.core.graph import run_workflow
from analytics_system.agents.visualization_agent import VisualizationAgent
from analytics_system.agents.ml_recommendation_agent import MLRecommendationAgent
from analytics_system.visualization.correlation_plots import correlation_heatmap
from analytics_system.reporting.report_builder import build_report_text
from analytics_system.reporting.pdf_exporter import create_pdf_report
from analytics_system.utils.file_handler import REPORT_DIR
from analytics_system.visualization.dashboard_components import show_metrics

st.set_page_config(page_title="AI Multi-Agent Data Analytics", page_icon="📊", layout="wide")
st.title("🤖 AI Multi-Agent Data Analytics Platform")
st.caption("Upload a CSV and let specialized agents profile, clean, analyze, visualize, and explain your data.")

with st.sidebar:
    st.header("1. Upload dataset")
    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    st.divider()
    st.header("2. Cleaning options")
    standardize = st.checkbox("Standardize column names", value=True)
    remove_duplicates = st.checkbox("Remove exact duplicate rows", value=True)
    fill_numeric = st.checkbox("Fill missing numeric values with median", value=True)
    fill_categorical = st.checkbox("Fill missing categorical values with mode", value=True)
    st.divider()
    request = st.text_area("Tell the Supervisor Agent what to do", value="Run full analysis, create useful visualizations, and summarize the findings.", height=110)
    run_button = st.button("🚀 Run analytics pipeline", type="primary", use_container_width=True)

if not uploaded:
    st.info("Upload a CSV file in the sidebar to begin.")
    st.markdown("### Included agents")
    st.write("Data Profiling · Data Cleaning · EDA · Visualization · Anomaly Detection · AI Insights · Report Generation")
    st.markdown("### Try it with a sales CSV")
    sample = pd.DataFrame({"Date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"], "Product": ["Laptop", "Phone", "Chair", "Laptop", "Phone"], "Category": ["Electronics", "Electronics", "Furniture", "Electronics", "Electronics"], "Quantity": [2, 5, 3, 1, 4], "Price": [50000, 15000, 3000, 50000, 15000], "Region": ["Kerala", "Tamil Nadu", "Kerala", "Karnataka", "Kerala"]})
    st.download_button("Download sample sales CSV", sample.to_csv(index=False).encode("utf-8"), "sample_sales.csv", "text/csv")
    st.stop()

try:
    original_df, validation_issues = ingest_uploaded_file(uploaded)
except Exception as exc:
    st.error(f"Could not load this CSV: {exc}")
    st.stop()

st.subheader("Original dataset preview")
st.caption(f"File: {uploaded.name} · Showing first 100 rows")
st.dataframe(original_df.head(100), use_container_width=True)

# Profile the original dataset immediately, even before the user runs cleaning.
from analytics_system.agents.data_profiling_agent import DataProfilingAgent
profile = DataProfilingAgent().run(original_df)
show_metrics(profile)
if validation_issues:
    st.warning("Data validation notes: " + " ".join(validation_issues))

with st.expander("Dataset profile details", expanded=False):
    left, right = st.columns(2)
    with left:
        st.write("**Column types**")
        st.json(profile["dtypes"])
    with right:
        st.write("**Columns with missing values**")
        st.json(profile["missing_by_column"] or {"message": "No missing values detected"})
    st.write("**Numeric columns:**", profile["numeric_columns"] or "None")
    st.write("**Categorical columns:**", profile["categorical_columns"] or "None")

if run_button:
    with st.spinner("Agents are working on your dataset..."):
        try:
            results = run_workflow(
                original_df,
                request=request,
                cleaning_options={
                    "drop_duplicates": remove_duplicates,
                    "fill_numeric": fill_numeric,
                    "fill_categorical": fill_categorical,
                    "standardize_column_names": standardize,
                },
                include_anomalies="anomal" in request.lower() or "outlier" in request.lower(),
            )
            st.session_state["analytics_results"] = results
            st.session_state["source_name"] = uploaded.name
        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")

results = st.session_state.get("analytics_results")
if results is not None:
    df_clean = results["cleaned_df"]
    st.success("Pipeline completed successfully.")
    st.subheader("Agent execution")
    st.write("Supervisor selected:", ", ".join(results.get("selected_agents", [])))
    tabs = st.tabs(["Cleaning report", "EDA", "Visualizations", "ML Agent", "Anomalies", "AI insights", "Downloads"])

    with tabs[0]:
        st.subheader("Cleaning summary")
        st.json(results.get("cleaning_report", {}))
        st.write("**Cleaned dataset preview**")
        st.dataframe(df_clean.head(200), use_container_width=True)
        st.caption("The original upload remains unchanged. Review these changes before using the cleaned data.")

    with tabs[1]:
        st.subheader("Descriptive statistics")
        st.write("**Numerical columns**")
        if not df_clean.select_dtypes(include="number").empty:
            st.dataframe(df_clean.describe(include="number").T, use_container_width=True)
        else:
            st.info("No numerical columns found.")
        st.write("**Categorical summaries**")
        for col in df_clean.select_dtypes(exclude="number").columns[:12]:
            with st.expander(str(col)):
                st.dataframe(df_clean[col].astype("string").value_counts(dropna=False).head(20).rename_axis("value").reset_index(name="count"), use_container_width=True)
        heatmap = correlation_heatmap(df_clean)
        if heatmap is not None:
            st.plotly_chart(heatmap, use_container_width=True)

    with tabs[2]:
        st.subheader("Interactive visualization studio")
        columns = list(df_clean.columns)
        numeric_cols = list(df_clean.select_dtypes(include="number").columns)
        c1, c2, c3 = st.columns(3)
        with c1:
            chart_type = st.selectbox("Chart type", ["Bar chart", "Line chart", "Scatter plot", "Histogram", "Box plot", "Pie chart"])
        with c2:
            x_col = st.selectbox("Category / X-axis", columns, index=0)
        with c3:
            y_options = ["(count only)"] + numeric_cols
            y_choice = st.selectbox("Value / Y-axis (optional)", y_options, index=1 if numeric_cols and chart_type in ["Bar chart", "Line chart", "Scatter plot"] else 0)
        y_col = None if y_choice == "(count only)" else y_choice
        if st.button("Generate chart"):
            try:
                fig = VisualizationAgent().run(df_clean, chart_type, x_col, y_col)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error(str(exc))
        st.markdown("#### Quick chart suggestions")
        if numeric_cols:
            for col in numeric_cols[:3]:
                st.plotly_chart(VisualizationAgent().run(df_clean, "Histogram", col), use_container_width=True)

    with tabs[3]:
        st.subheader("Machine Learning Recommendation Agent")
        st.write("Choose a target column for supervised learning, or explore unsupervised techniques when no target is available.")
        ml_agent = MLRecommendationAgent()
        ml_target_options = ["(No target / unsupervised)"] + list(df_clean.columns)
        ml_target_choice = st.selectbox("Target column (what you want to predict)", ml_target_options, key="ml_target")
        ml_target = None if ml_target_choice == "(No target / unsupervised)" else ml_target_choice
        ml_task_options = ["Auto-detect", "Classification", "Regression", "Clustering", "Anomaly Detection"]
        ml_task = st.selectbox("ML task", ml_task_options, key="ml_task")
        if st.button("Recommend ML techniques", key="recommend_ml"):
            try:
                ml_result = ml_agent.recommend(df_clean, target=ml_target, task=ml_task)
                st.session_state["ml_recommendations"] = ml_result
            except Exception as exc:
                st.error(f"Could not recommend techniques: {exc}")
        ml_result = st.session_state.get("ml_recommendations")
        if ml_result:
            st.markdown(f"**Detected task:** {ml_result['task']}")
            st.write(ml_result["target_summary"])
            for i, rec in enumerate(ml_result["recommendations"], start=1):
                with st.expander(f"{i}. {rec['technique']}", expanded=(i == 1)):
                    st.write("**Why it may fit:**", rec["why"])
                    st.write("**Advantages / considerations:**", rec["pros"])
            if ml_result["warnings"]:
                for warning in ml_result["warnings"]:
                    st.warning(warning)
            st.caption(ml_result["note"])
            if ml_target and ml_result["task"] in ("Classification", "Regression"):
                model_options = ["Recommended baseline", "Logistic Regression", "Random Forest Classifier"] if ml_result["task"] == "Classification" else ["Recommended baseline", "Linear Regression", "Random Forest Regressor"]
                chosen_model = st.selectbox("Model to train", model_options, key="ml_model_choice")
                if st.button("Train and evaluate baseline model", key="train_ml"):
                    try:
                        training = ml_agent.train_baseline(df_clean, ml_target, ml_result["task"], chosen_model)
                        st.session_state["ml_training_results"] = training
                    except Exception as exc:
                        st.error(f"Model training failed: {exc}")
            training = st.session_state.get("ml_training_results")
            if training:
                st.markdown("#### Evaluation results")
                st.write(f"**Model:** {training['model']} · **Task:** {training['task']} · **Target:** {training['target']}")
                metric_cols = st.columns(len(training["metrics"]))
                for col, (metric, value) in zip(metric_cols, training["metrics"].items()):
                    col.metric(metric.replace("_", " ").title(), value)
                st.caption(f"Train rows: {training['train_rows']} · Test rows: {training['test_rows']}")
                st.write("**Features used:**", ", ".join(training["features_used"]))
                st.info("Metrics are from a single holdout split. Compare models and consider cross-validation before using a model in production.")

    with tabs[4]:
        st.subheader("Anomaly detection")
        anomaly_df = results.get("anomalies")
        if anomaly_df is None:
            st.info("No anomaly detection was requested. Add 'anomaly' or 'outlier' to your request and run the pipeline again.")
        else:
            count = int(anomaly_df["_is_anomaly"].sum())
            st.metric("Potential anomalies flagged", count)
            st.caption("Flags are candidates for review, not proof of errors. Isolation Forest uses numerical columns only.")
            st.dataframe(anomaly_df[anomaly_df["_is_anomaly"]].head(200), use_container_width=True)
            st.download_button("Download anomaly results CSV", anomaly_df.to_csv(index=False).encode("utf-8"), "anomaly_results.csv", "text/csv")

    with tabs[5]:
        st.subheader("Insights Agent")
        st.markdown(results.get("insights", "No insights generated."))
        st.caption("For LLM-powered explanations, configure OPENAI_API_KEY in .env. Without it, a deterministic summary is shown.")

    with tabs[6]:
        st.subheader("Download outputs")
        st.download_button("Download cleaned CSV", df_clean.to_csv(index=False).encode("utf-8-sig"), "cleaned_dataset.csv", "text/csv", use_container_width=True)
        report_text = build_report_text(results)
        st.download_button("Download report as TXT", report_text.encode("utf-8"), "analytics_report.txt", "text/plain", use_container_width=True)
        if st.button("Generate PDF report"):
            try:
                output = REPORT_DIR / "analytics_report.pdf"
                create_pdf_report(report_text, str(output))
                st.session_state["pdf_report_path"] = str(output)
            except Exception as exc:
                st.error(f"PDF report generation failed: {exc}")
        pdf_path = st.session_state.get("pdf_report_path")
        if pdf_path and Path(pdf_path).exists():
            st.download_button("Download PDF report", Path(pdf_path).read_bytes(), "analytics_report.pdf", "application/pdf", use_container_width=True)
