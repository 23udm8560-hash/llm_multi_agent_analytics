import pandas as pd
import plotly.express as px


def make_chart(df: pd.DataFrame, chart_type: str, x: str, y: str | None = None):
    if x not in df.columns:
        raise ValueError(f"Column not found: {x}")
    if y and y not in df.columns:
        raise ValueError(f"Column not found: {y}")
    if chart_type == "Bar chart":
        if y:
            data = df.groupby(x, dropna=False, as_index=False)[y].sum().sort_values(y, ascending=False).head(50)
            return px.bar(data, x=x, y=y, title=f"{y} by {x}")
        counts = df[x].astype("string").value_counts().head(30).rename_axis(x).reset_index(name="count")
        return px.bar(counts, x=x, y="count", title=f"Count by {x}")
    if chart_type == "Line chart":
        if not y:
            raise ValueError("Select a Y-axis column for a line chart.")
        data = df[[x, y]].copy()
        if pd.api.types.is_datetime64_any_dtype(data[x]):
            data = data.sort_values(x)
        return px.line(data, x=x, y=y, title=f"{y} over {x}")
    if chart_type == "Scatter plot":
        if not y:
            raise ValueError("Select a Y-axis column for a scatter plot.")
        return px.scatter(df, x=x, y=y, title=f"{y} vs {x}")
    if chart_type == "Histogram":
        return px.histogram(df, x=x, title=f"Distribution of {x}")
    if chart_type == "Box plot":
        return px.box(df, x=x if y else None, y=y or x, title=f"Box plot: {y or x}")
    if chart_type == "Pie chart":
        counts = df[x].astype("string").value_counts().head(15).rename_axis(x).reset_index(name="count")
        return px.pie(counts, names=x, values="count", title=f"Composition by {x}")
    raise ValueError("Unsupported chart type.")
