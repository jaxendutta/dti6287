"""
config.py — Single source of truth for all project constants.

Every script and notebook imports from here. Nothing is hardcoded elsewhere.
Machine-specific overrides go in .env (see .env.example).
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env overrides ───────────────────────────────────────────────────────
load_dotenv()

# ── Paths ─────────────────────────────────────────────────────────────────────
# src/bi/config.py → go up two levels to reach project root
ROOT          = Path(__file__).parent.parent.parent
DATA_DIR      = ROOT / "data"
OUTPUT_DIR    = ROOT / "output"
NOTEBOOKS_DIR = ROOT / "notebooks"
SCRIPTS_DIR   = ROOT / "scripts"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Dataset ───────────────────────────────────────────────────────────────────
KAGGLE_DATASET_SLUG = "mexwell/carrier-on-time-performance-dataset"
DOWNLOAD_URL        = f"https://www.kaggle.com/api/v1/datasets/download/{KAGGLE_DATASET_SLUG}"
DOWNLOAD_ZIP        = DATA_DIR / "carrier-on-time-performance-dataset.zip"
RAW_CSV             = DATA_DIR / "airline_2m.csv"
CLEANED_PARQUET     = OUTPUT_DIR / "airline_cleaned.parquet"
SPARK_PARQUET       = OUTPUT_DIR / "airline_cleaned_spark"

# BTS data contains Latin-1 encoded characters in some city/airport name fields
CSV_ENCODING     = "latin-1"    # used by pandas
SPARK_CSV_ENCODING = "iso-8859-1"  # same encoding, Spark's name for it

# ── Spark ─────────────────────────────────────────────────────────────────────
SPARK_APP_NAME           = "AirlineOnTime-Analytics"
SPARK_DRIVER_MEMORY      = os.getenv("SPARK_DRIVER_MEMORY", "4g")
SPARK_SHUFFLE_PARTITIONS = int(os.getenv("SPARK_SHUFFLE_PARTITIONS", "8"))
SPARK_PYTHON = sys.executable  # use the exact Python running this script

# ── Column groups ─────────────────────────────────────────────────────────────
DROP_COLS = [
    "OriginAirportSeqID", "OriginCityMarketID", "OriginWac",
    "DestAirportSeqID",   "DestCityMarketID",   "DestWac",
    "DOT_ID_Reporting_Airline", "IATA_CODE_Reporting_Airline",
    "Div3Airport", "Div3AirportID", "Div3AirportSeqID", "Div3WheelsOn",
    "Div3TotalGTime", "Div3LongestGTime", "Div3WheelsOff", "Div3TailNum",
    "Div4Airport", "Div4AirportID", "Div4AirportSeqID", "Div4WheelsOn",
    "Div4TotalGTime", "Div4LongestGTime", "Div4WheelsOff", "Div4TailNum",
    "Div5Airport", "Div5AirportID", "Div5AirportSeqID", "Div5WheelsOn",
    "Div5TotalGTime", "Div5LongestGTime", "Div5WheelsOff", "Div5TailNum",
]

CORE_COLS = ["Year", "Month", "Origin", "Dest", "Reporting_Airline"]

INT_COLS = [
    "Year", "Quarter", "Month", "DayofMonth", "DayOfWeek",
    "CRSDepTime", "DepTime", "CRSArrTime", "ArrTime",
    "DepDel15", "ArrDel15", "Cancelled", "Diverted", "DistanceGroup",
]

DOUBLE_COLS = [
    "DepDelay", "DepDelayMinutes", "ArrDelay", "ArrDelayMinutes",
    "TaxiOut", "TaxiIn", "CRSElapsedTime", "ActualElapsedTime", "AirTime",
    "Distance",
    "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
]

# ── Data quality thresholds ───────────────────────────────────────────────────
DELAY_MIN_MINUTES   = -360
DELAY_MAX_MINUTES   =  1440
MIN_CARRIER_FLIGHTS =  5_000

# ── Plotting ──────────────────────────────────────────────────────────────────
FIGURE_DPI    = 150
FIGURE_SIZE   = (12, 5)

COLOR_PRIMARY = "steelblue"
COLOR_DELAY   = "tomato"
COLOR_GOOD    = "mediumseagreen"

# ── Target variable ───────────────────────────────────────────────────────────
TARGET_COL = "IsDelayed"

# ── Feature engineering ───────────────────────────────────────────────────────
MONTH_TO_SEASON = {
    12: 1, 1: 1, 2: 1,
     3: 2, 4: 2, 5: 2,
     6: 3, 7: 3, 8: 3,
     9: 4, 10: 4, 11: 4,
}

DOW_LABELS   = {1:"Mon", 2:"Tue", 3:"Wed", 4:"Thu", 5:"Fri", 6:"Sat", 7:"Sun"}
MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]