from analytics_system.agents.data_cleaning_agent import DataCleaningAgent


def run_cleaning_pipeline(df, **options):
    return DataCleaningAgent().run(df, **options)
