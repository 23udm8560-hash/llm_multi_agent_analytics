from pathlib import Path
from analytics_system.agents.report_generation_agent import ReportGenerationAgent


def run_reporting_pipeline(results: dict, output_path="data/reports/analytics_report.pdf"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return ReportGenerationAgent().run(results, output_path)
