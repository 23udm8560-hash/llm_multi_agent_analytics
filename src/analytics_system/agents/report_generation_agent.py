from analytics_system.reporting.report_builder import build_report_text
from analytics_system.reporting.pdf_exporter import create_pdf_report


class ReportGenerationAgent:
    name = "Report Generation Agent"

    def run(self, results: dict, output_path: str):
        text = build_report_text(results)
        create_pdf_report(text, output_path)
        return output_path
