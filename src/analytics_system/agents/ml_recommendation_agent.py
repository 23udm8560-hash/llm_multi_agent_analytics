"""Recommend and optionally train baseline ML models for uploaded tabular data."""
from __future__ import annotations

from typing import Any
import pandas as pd


class MLRecommendationAgent:
    name = "Machine Learning Recommendation Agent"

    def recommend(self, df: pd.DataFrame, target: str | None = None, task: str = "Auto-detect") -> dict[str, Any]:
        if df is None or df.empty:
            raise ValueError("Upload a non-empty dataset first.")

        numeric_cols = list(df.select_dtypes(include="number").columns)
        categorical_cols = list(df.select_dtypes(include=["object", "category", "bool", "string"]).columns)
        recommendations: list[dict[str, str]] = []
        inferred_task = task
        target_summary = "No target column selected; use unsupervised methods unless you choose a prediction target."

        if target and target in df.columns:
            y = df[target].dropna()
            unique_count = int(y.nunique())
            if task == "Auto-detect":
                # A small-cardinality target is treated as classification; otherwise regression.
                if (not pd.api.types.is_numeric_dtype(y)) or unique_count <= min(20, max(2, int(len(y) * 0.05))):
                    inferred_task = "Classification"
                else:
                    inferred_task = "Regression"
            target_summary = f"Target: {target}; non-null values: {len(y)}; unique values: {unique_count}."

        if inferred_task == "Auto-detect":
            inferred_task = "Clustering / unsupervised learning"

        if inferred_task == "Classification":
            recommendations = [
                {"technique": "Logistic Regression", "why": "A strong, interpretable baseline for classification, especially when relationships are relatively simple.", "pros": "Fast; interpretable; useful baseline."},
                {"technique": "Random Forest Classifier", "why": "Captures nonlinear relationships and feature interactions with limited feature scaling requirements.", "pros": "Robust baseline; handles mixed patterns."},
                {"technique": "Decision Tree Classifier", "why": "Useful when you need a model whose decision rules can be inspected.", "pros": "Easy to explain; little preprocessing."},
            ]
        elif inferred_task == "Regression":
            recommendations = [
                {"technique": "Linear Regression", "why": "An interpretable baseline when the target has a reasonably linear relationship with the predictors.", "pros": "Fast; coefficients are interpretable."},
                {"technique": "Random Forest Regressor", "why": "Can model nonlinear relationships and interactions without requiring feature scaling.", "pros": "Flexible baseline; captures nonlinear patterns."},
                {"technique": "Decision Tree Regressor", "why": "Useful for exploring nonlinear rules and threshold-like relationships.", "pros": "Easy to inspect; minimal scaling needs."},
            ]
        elif inferred_task in ("Clustering", "Clustering / unsupervised learning"):
            recommendations = [
                {"technique": "K-Means", "why": "A useful first clustering method for numeric, scaled features when you can choose the number of clusters.", "pros": "Fast and easy to compare; scale features first."},
                {"technique": "DBSCAN", "why": "Can find dense groups and mark some observations as noise without preselecting cluster count.", "pros": "Can detect irregular-shaped clusters; sensitive to parameters and scaling."},
                {"technique": "Agglomerative Clustering", "why": "Useful for exploring hierarchical groupings in small or medium datasets.", "pros": "Provides hierarchical structure; can be costly on large datasets."},
            ]
        elif inferred_task in ("Anomaly Detection", "Anomaly detection"):
            recommendations = [
                {"technique": "Isolation Forest", "why": "A practical unsupervised baseline for flagging unusual numeric observations.", "pros": "Works across multiple numeric features; tune contamination carefully."},
                {"technique": "Local Outlier Factor", "why": "Flags observations that are locally less dense than their neighbors.", "pros": "Can detect local anomalies; sensitive to scaling and neighbor count."},
            ]
        else:
            raise ValueError(f"Unsupported task: {inferred_task}")

        warnings = []
        if target and target in df.columns:
            if df[target].isna().any():
                warnings.append("Rows with missing target values must be excluded or reviewed before training.")
            if df[target].nunique(dropna=True) < 2 and inferred_task == "Classification":
                warnings.append("The selected target has fewer than two classes; classification training is not possible yet.")
            if target in numeric_cols:
                numeric_predictors = [c for c in numeric_cols if c != target]
            else:
                numeric_predictors = numeric_cols
        else:
            numeric_predictors = numeric_cols
        if not numeric_predictors and inferred_task in ("Classification", "Regression"):
            warnings.append("No numeric predictor columns were detected; categorical columns can still be used by the training pipeline.")
        if len(df) < 30:
            warnings.append("Small dataset: evaluation metrics may be unstable. Treat model scores as exploratory.")

        return {
            "agent": self.name,
            "task": inferred_task,
            "target": target,
            "target_summary": target_summary,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "recommendations": recommendations,
            "warnings": warnings,
            "note": "Recommendations are candidates, not guarantees. Compare models using a suitable validation strategy and domain knowledge.",
        }

    def train_baseline(self, df: pd.DataFrame, target: str, task: str = "Auto-detect", model_name: str = "Recommended baseline") -> dict[str, Any]:
        """Train a baseline supervised model and return metrics plus a fitted pipeline."""
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
        from sklearn.linear_model import LogisticRegression, LinearRegression
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        import numpy as np

        if target not in df.columns:
            raise ValueError("Select a valid target column.")
        working = df.dropna(subset=[target]).copy()
        if len(working) < 10:
            raise ValueError("At least 10 rows with non-missing target values are recommended for baseline training.")
        y = working[target]
        if task == "Auto-detect":
            if (not pd.api.types.is_numeric_dtype(y)) or y.nunique() <= min(20, max(2, int(len(y) * 0.05))):
                task = "Classification"
            else:
                task = "Regression"
        if task not in ("Classification", "Regression"):
            raise ValueError("Baseline training currently supports Classification or Regression. Use recommendations for clustering and anomaly detection.")

        X = working.drop(columns=[target]).copy()
        # Drop entirely empty and constant predictors; keep target out of features.
        X = X.dropna(axis=1, how="all")
        X = X.loc[:, X.nunique(dropna=False) > 1]
        if X.empty:
            raise ValueError("No useful predictor columns remain after removing empty/constant columns.")
        # Convert datetimes to string categories to avoid unsupported raw datetime input.
        for col in X.columns:
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                X[col] = X[col].astype("string")
        numeric = list(X.select_dtypes(include="number").columns)
        categorical = [c for c in X.columns if c not in numeric]
        transformers = []
        if numeric:
            numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
            transformers.append(("numeric", numeric_pipe, numeric))
        if categorical:
            categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])
            transformers.append(("categorical", categorical_pipe, categorical))
        preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

        if task == "Classification":
            if y.nunique() < 2:
                raise ValueError("The target must contain at least two classes.")
            counts = y.value_counts()
            stratify = y if counts.min() >= 2 and y.nunique() < len(y) * 0.5 else None
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=stratify)
            if model_name == "Logistic Regression":
                estimator = LogisticRegression(max_iter=1000, class_weight="balanced")
            else:
                estimator = RandomForestClassifier(n_estimators=150, random_state=42, class_weight="balanced")
            pipeline = Pipeline([("preprocessor", preprocessor), ("model", estimator)])
            pipeline.fit(X_train, y_train)
            pred = pipeline.predict(X_test)
            metrics = {"accuracy": round(float(accuracy_score(y_test, pred)), 4), "weighted_f1": round(float(f1_score(y_test, pred, average="weighted", zero_division=0)), 4)}
        else:
            y = pd.to_numeric(y, errors="coerce")
            valid = y.notna()
            X, y = X.loc[valid], y.loc[valid]
            if len(y) < 10:
                raise ValueError("Not enough valid numeric target rows for regression.")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            estimator = LinearRegression() if model_name == "Linear Regression" else RandomForestRegressor(n_estimators=150, random_state=42)
            pipeline = Pipeline([("preprocessor", preprocessor), ("model", estimator)])
            pipeline.fit(X_train, y_train)
            pred = pipeline.predict(X_test)
            rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
            metrics = {"mae": round(float(mean_absolute_error(y_test, pred)), 4), "rmse": round(rmse, 4), "r2": round(float(r2_score(y_test, pred)), 4)}

        return {"task": task, "target": target, "model": model_name, "metrics": metrics, "train_rows": int(len(X_train)), "test_rows": int(len(X_test)), "features_used": list(X.columns), "pipeline": pipeline}
