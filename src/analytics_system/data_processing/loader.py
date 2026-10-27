from io import BytesIO, StringIO
import pandas as pd


def load_csv(uploaded_file) -> pd.DataFrame:
    """Load a Streamlit UploadedFile or bytes buffer with encoding fallbacks."""
    raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file
    errors = []
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(BytesIO(raw), encoding=encoding, low_memory=False)
        except Exception as exc:
            errors.append(f"{encoding}: {exc}")
    raise ValueError("Could not read CSV. Details: " + " | ".join(errors))
