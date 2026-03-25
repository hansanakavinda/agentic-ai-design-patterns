import pandas as pd
import json
import base64
import mimetypes
from pathlib import Path
import re

# === Data Loading ===
def load_and_prepare_data(csv_path: str) -> pd.DataFrame:
    """Load CSV and derive date parts commonly used in charts."""
    df = pd.read_csv(csv_path)
    # Be tolerant if 'date' exists
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["quarter"] = df["date"].dt.quarter
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
    return df

def extract_code(response):
    data = json.loads(response)
    code = data["python_code"]
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", code)
    if match:
        code = match.group(1).strip()
    return code

def execute_chart_code(code, df):
    error = None
    exec_globals = {"df": df}
    try:
        exec(code, exec_globals)
    except Exception as e:
        error = e
    return error

def encode_image_b64(path: str) -> tuple[str, str]:
    """Return (media_type, base64_str) for an image file path."""
    mime, _ = mimetypes.guess_type(path)
    media_type = mime or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return media_type, b64
