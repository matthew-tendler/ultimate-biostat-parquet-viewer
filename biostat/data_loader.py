import pyarrow.parquet as pq
import io
import pandas as pd

def load_parquet_file(uploaded_file):
    # Read uploaded file contents as bytes
    raw_bytes = uploaded_file.read()

    # Wrap in a BytesIO buffer so PyArrow can read it
    buffer = io.BytesIO(raw_bytes)

    # Load Parquet into a PyArrow table
    table = pq.read_table(buffer)

    # Convert to pandas DataFrame preserving true nulls
    df = table.to_pandas(types_mapper=pd.ArrowDtype)

    # Convert empty and whitespace-only strings to proper missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    return df