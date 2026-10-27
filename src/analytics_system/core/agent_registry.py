from analytics_system.agents.data_profiling_agent import DataProfilingAgent
from analytics_system.agents.data_cleaning_agent import DataCleaningAgent
from analytics_system.agents.eda_agent import EDAAgent
from analytics_system.agents.visualization_agent import VisualizationAgent
from analytics_system.agents.statistical_analysis_agent import StatisticalAnalysisAgent
from analytics_system.agents.anomaly_detection_agent import AnomalyDetectionAgent
from analytics_system.agents.insights_agent import InsightsAgent
from analytics_system.agents.report_generation_agent import ReportGenerationAgent
from analytics_system.agents.supervisor_agent import SupervisorAgent
from analytics_system.agents.ml_recommendation_agent import MLRecommendationAgent


def build_agents():
    return {
        "supervisor": SupervisorAgent(),
        "profiling": DataProfilingAgent(),
        "cleaning": DataCleaningAgent(),
        "eda": EDAAgent(),
        "visualization": VisualizationAgent(),
        "statistics": StatisticalAnalysisAgent(),
        "anomaly": AnomalyDetectionAgent(),
        "insights": InsightsAgent(),
        "report": ReportGenerationAgent(),
        "ml_recommendation": MLRecommendationAgent(),
    }
