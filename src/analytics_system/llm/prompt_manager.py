try:
    from templates.prompts import INSIGHTS_SYSTEM_PROMPT
except ImportError:
    INSIGHTS_SYSTEM_PROMPT = (
        "You are a careful data analyst. Explain only supplied calculated results. "
        "Do not invent numbers or claim causation from correlation. State limitations."
    )


def build_insights_prompt(results: dict, user_question: str = "") -> str:
    return f"""{INSIGHTS_SYSTEM_PROMPT}

User question: {user_question or 'Summarize the dataset analysis.'}
Calculated results (JSON-like data):
{results}

Give a concise answer. Only report figures present in the calculated results. Mention limitations."""
