"""Workflow orchestration. Uses LangGraph when installed; otherwise a deterministic fallback."""
from analytics_system.core.agent_registry import build_agents
from analytics_system.logging.logger import logger


def run_workflow(df, request="Run full analysis", cleaning_options=None, include_anomalies=False):
    agents = build_agents()
    selected = agents["supervisor"].select_agents(request)
    state = {"original_df": df.copy(), "cleaned_df": df.copy(), "user_request": request, "selected_agents": selected, "errors": [], "status": "running"}
    try:
        state["profile"] = agents["profiling"].run(state["original_df"])
        if "cleaning" in selected:
            opts = cleaning_options or {}
            state["cleaned_df"], state["cleaning_report"] = agents["cleaning"].run(state["original_df"], **opts)
        else:
            state["cleaning_report"] = {"actions": ["Cleaning skipped by request"], "duplicates_removed": 0, "numeric_cells_filled": 0, "categorical_cells_filled": 0, "rows_before": len(df), "rows_after": len(df), "missing_remaining": int(df.isna().sum().sum())}
        state["eda"] = agents["eda"].run(state["cleaned_df"])
        if include_anomalies or "anomaly" in selected:
            state["anomalies"] = agents["anomaly"].run(state["cleaned_df"])
        insight_input = {"profile": state["profile"], "cleaning_report": state["cleaning_report"], "eda": state["eda"]}
        state["insights"] = agents["insights"].run(insight_input, request)
        state["status"] = "completed"
        logger.info("Workflow completed. Agents: %s", selected)
    except Exception as exc:
        state["errors"].append(str(exc))
        state["status"] = "failed"
        logger.exception("Workflow failed")
        raise
    return state


def build_langgraph_app():
    """Build a small LangGraph graph for visibility/extension; master workflow uses tested Python orchestration."""
    try:
        from langgraph.graph import StateGraph, START, END
        from analytics_system.core.state import AnalyticsState
        from analytics_system.agents.data_profiling_agent import DataProfilingAgent
        from analytics_system.agents.data_cleaning_agent import DataCleaningAgent
        from analytics_system.agents.eda_agent import EDAAgent
        profiling, cleaning, eda = DataProfilingAgent(), DataCleaningAgent(), EDAAgent()
        graph = StateGraph(AnalyticsState)
        graph.add_node("profiling", lambda s: {"profile": profiling.run(s["original_df"])})
        graph.add_node("cleaning", lambda s: {"cleaned_df": cleaning.run(s["original_df"])[0], "cleaning_report": cleaning.run(s["original_df"])[1]})
        graph.add_node("eda", lambda s: {"eda": eda.run(s.get("cleaned_df", s["original_df"]))})
        graph.add_edge(START, "profiling")
        graph.add_edge("profiling", "cleaning")
        graph.add_edge("cleaning", "eda")
        graph.add_edge("eda", END)
        return graph.compile()
    except ImportError:
        return None
