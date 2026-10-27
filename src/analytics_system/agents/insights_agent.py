from analytics_system.llm.llm_client import get_llm
from analytics_system.llm.prompt_manager import build_insights_prompt
from analytics_system.llm.response_parser import response_to_text


class InsightsAgent:
    name = "Insights Agent"

    def run(self, results: dict, user_question: str = "") -> str:
        llm = get_llm()
        if llm is not None:
            try:
                response = llm.invoke(build_insights_prompt(results, user_question))
                return response_to_text(response)
            except Exception as exc:
                return (
                    f"LLM request failed; showing rule-based summary instead. Details: {exc}\n\n"
                    f"{self._fallback(results)}"
                )
        return self._fallback(results)

    @staticmethod
    def _fallback(results: dict) -> str:
        profile = results.get("profile", {})
        cleaning = results.get("cleaning_report", {})
        stats = results.get("eda", {}).get("descriptive_statistics", {})
        lines = [
            "## Analysis summary",
            f"- Dataset contains {profile.get('rows', 0):,} rows and {profile.get('columns', 0):,} columns.",
            f"- The original dataset has {profile.get('missing_total', 0):,} missing cells and {profile.get('duplicate_rows', 0):,} duplicate rows.",
            f"- Cleaning removed {cleaning.get('duplicates_removed', 0):,} duplicate rows and filled {cleaning.get('numeric_cells_filled', 0) + cleaning.get('categorical_cells_filled', 0):,} missing cells where selected strategies applied.",
        ]
        if stats.get("numeric_summary"):
            lines.append("- Numeric summary statistics are available in the EDA tab; review the ranges and distributions before drawing conclusions.")
        lines.append("- These results describe the uploaded data and do not by themselves prove causation or guarantee data accuracy.")
        lines.append("\nSet OPENAI_API_KEY in your .env file to enable LLM-generated explanations.")
        return "\n".join(lines)
