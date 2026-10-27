from analytics_system.core.graph import run_workflow


def run_master_pipeline(df, request="Run full analysis", cleaning_options=None, include_anomalies=False):
    return run_workflow(df, request, cleaning_options, include_anomalies)
