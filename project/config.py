from pathlib import Path

# Katalog główny projektu
BASE_DIR = Path(".")

# Baza danych
DATABASE_PATH = BASE_DIR / "data" / "raw" / "patients.db"

# Dane przetworzone
PROCESSED_PATH = BASE_DIR / "data" / "processed"

# Wyniki
RESULTS_PATH = BASE_DIR / "results"

TABLES_PATH = RESULTS_PATH / "tables"

PLOTS_PATH = RESULTS_PATH / "plots"

# Statystyki
INPUT_STATS_PATH = TABLES_PATH / "input_stats.csv"

OUTPUT_STATS_PATH = TABLES_PATH / "output_stats.csv"

# Parametry agregacji i grupowania

AGGREGATION_METHODS = ["mean", "median"]
GROUP_BY_COLUMN = ["gender"]


# Kolumny
PATIENT_ID_COLUMN = "patient_id"
VISIT_ID_COLUMN = "visit_id"
TIME_COLUMN = "visit_date"

STATIC_COLUMNS = ["age", "gender", "class"]

EXCLUDE_COLUMNS = [
    PATIENT_ID_COLUMN,
    VISIT_ID_COLUMN,
    "class",
    "gender"
]

FEATURE_COLUMNS = [
    "BMI",
    "HDL",
    "LDL",
    "Urea",
    "TG",
    "Chol",
    "Cr",
    "HbA1c",
    "VLDL"
]
