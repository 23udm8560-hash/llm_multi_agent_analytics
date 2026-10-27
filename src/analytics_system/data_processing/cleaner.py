import pandas as pd
import numpy as np


def clean_dataframe(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_numeric: bool = True,
    fill_categorical: bool = True,
    standardize_column_names: bool = True,
) -> tuple[pd.DataFrame, dict]:
    """Return a cleaned copy and an auditable summary. Never mutates the original."""
    cleaned = df.copy(deep=True)
    report = {"rows_before": int(len(cleaned)), "columns_before": int(len(cleaned.columns)), "duplicates_removed": 0, "numeric_cells_filled": 0, "categorical_cells_filled": 0, "column_names_standardized": False, "actions": []}

    if standardize_column_names:
        new_names = []
        for col in cleaned.columns:
            name = str(col).strip().lower()
            name = "_".join(name.replace("-", " ").replace("/", " ").split())
            new_names.append(name or "unnamed_column")
        # Ensure names are unique after normalization.
        seen, unique_names = {}, []
        for name in new_names:
            count = seen.get(name, 0)
            unique_names.append(name if count == 0 else f"{name}_{count + 1}")
            seen[name] = count + 1
        if list(cleaned.columns) != unique_names:
            cleaned.columns = unique_names
            report["column_names_standardized"] = True
            report["actions"].append("Standardized column names")

    if drop_duplicates:
        before = len(cleaned)
        cleaned = cleaned.drop_duplicates().copy()
        report["duplicates_removed"] = int(before - len(cleaned))
        if before != len(cleaned):
            report["actions"].append("Removed exact duplicate rows")

    numeric_cols = list(cleaned.select_dtypes(include=np.number).columns)
    if fill_numeric:
        for col in numeric_cols:
            count = int(cleaned[col].isna().sum())
            if count:
                median = cleaned[col].median()
                if pd.notna(median):
                    cleaned[col] = cleaned[col].fillna(median)
                    report["numeric_cells_filled"] += count
        if report["numeric_cells_filled"]:
            report["actions"].append("Filled missing numeric values with column medians")

    if fill_categorical:
        categorical_cols = list(cleaned.select_dtypes(include=["object", "category", "string", "bool"]).columns)
        for col in categorical_cols:
            count = int(cleaned[col].isna().sum())
            if count:
                mode = cleaned[col].mode(dropna=True)
                replacement = mode.iloc[0] if not mode.empty else "Unknown"
                cleaned[col] = cleaned[col].fillna(replacement)
                report["categorical_cells_filled"] += count
        if report["categorical_cells_filled"]:
            report["actions"].append("Filled missing categorical values with the most frequent value")

    report["rows_after"] = int(len(cleaned))
    report["columns_after"] = int(len(cleaned.columns))
    report["missing_remaining"] = int(cleaned.isna().sum().sum())
    report["rows_removed"] = report["rows_before"] - report["rows_after"]
    return cleaned, report
