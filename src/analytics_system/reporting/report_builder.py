import json


def build_report_text(results: dict) -> str:
    profile = results.get("profile", {})
    cleaning = results.get("cleaning_report", {})
    eda = results.get("eda", {})
    lines = [
        "AI MULTI-AGENT DATA ANALYTICS REPORT",
        "=" * 42,
        "",
        "DATASET PROFILE",
        f"Rows: {profile.get('rows', 'N/A')}",
        f"Columns: {profile.get('columns', 'N/A')}",
        f"Missing cells: {profile.get('missing_total', 'N/A')}",
        f"Duplicate rows: {profile.get('duplicate_rows', 'N/A')}",
        "",
        "CLEANING SUMMARY",
        f"Rows before: {cleaning.get('rows_before', 'N/A')}",
        f"Rows after: {cleaning.get('rows_after', 'N/A')}",
        f"Duplicates removed: {cleaning.get('duplicates_removed', 0)}",
        f"Numeric cells filled: {cleaning.get('numeric_cells_filled', 0)}",
        f"Categorical cells filled: {cleaning.get('categorical_cells_filled', 0)}",
        "",
        "INSIGHTS",
        results.get("insights", "No insights available."),
        "",
        "EDA RESULTS",
        json.dumps(eda, indent=2, default=str)[:12000],
        "",
        "LIMITATIONS",
        "Automated findings may require domain review. Anomalies are flags for investigation, not proof of errors. Correlation does not establish causation.",
    ]
    return "\n".join(lines)
