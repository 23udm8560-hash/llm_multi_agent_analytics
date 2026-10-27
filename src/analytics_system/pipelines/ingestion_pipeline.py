from analytics_system.data_processing.loader import load_csv
from analytics_system.data_processing.validator import basic_validation
from analytics_system.utils.validators import validate_dataframe


def ingest_uploaded_file(uploaded_file):
    df = load_csv(uploaded_file)
    validate_dataframe(df)
    issues = basic_validation(df)
    return df, issues
