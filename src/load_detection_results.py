from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

password = quote_plus("21@21$")

DATABASE_URL = (
    f"postgresql://postgres:{password}@localhost:5432/medical_warehouse"
)

engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/processed/detection_results.csv")

print(df.head())

df.to_sql(
    "image_detections",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print("\nLoaded detection results successfully!")