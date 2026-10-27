# LLM Multi-Agent Data Analytics Platform

A Streamlit app for uploading CSV files and running a modular multi-agent analytics workflow: profiling, cleaning, EDA, visualizations, anomaly detection, LLM insights (optional), and PDF/CSV exports.

## 1. Setup (Windows PowerShell)

```powershell
cd llm_multi_agent_analytics
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

You can use the app without an API key. Add `OPENAI_API_KEY` and `OPENAI_MODEL` to `.env` to enable LLM explanations. Do not commit `.env` to GitHub.

## 2. How to use
1. Upload a CSV in the sidebar.
2. Review the profile and missing/duplicate-value report.
3. Choose cleaning options and click **Run analytics pipeline**.
4. Inspect the cleaned dataset, charts, anomaly flags, and AI insights.
5. Download the cleaned CSV or PDF report.

## 3. Architecture
- `agents/`: specialist agents
- `core/`: shared state and workflow orchestration
- `data_processing/`: deterministic CSV profiling and cleaning
- `pipelines/`: ingestion and master pipeline
- `llm/`: optional OpenAI integration
- `visualization/`: chart generation
- `reporting/`: PDF report creation

The LLM explains calculated results; Pandas/Scikit-learn perform actual calculations. Always review suggested cleaning actions before using the output for important decisions.


## Machine Learning Recommendation Agent

The **ML Agent** tab recommends techniques based on the selected task and dataset. Select a target column to identify a supervised learning task (classification or regression), or select no target to explore clustering methods. Recommendations explain why a technique may fit. For classification/regression, you can also train a baseline model and view holdout metrics.

Supported recommendations include Logistic Regression, Random Forest, Decision Trees, Linear Regression, K-Means, DBSCAN, Agglomerative Clustering, Isolation Forest, and Local Outlier Factor. Baseline training currently supports classification and regression only; clustering/anomaly techniques are recommendation-only in this starter version.

**Important:** Automatic task identification is heuristic. Confirm the target meaning and task before training. A single train/test split is exploratory and is not a substitute for cross-validation or domain validation.
