import sqlite3
import pandas as pd
from project.config import DATABASE_PATH


def load_data():
    try:

        conn = sqlite3.connect(DATABASE_PATH)

        patients = pd.read_sql("SELECT * FROM patients", conn)
        visits = pd.read_sql("SELECT * FROM visits", conn)
        measurements = pd.read_sql("SELECT * FROM measurements", conn)

        conn.close()

        return (patients, visits, measurements)

    except sqlite3.OperationalError as e:
        raise sqlite3.DatabaseError(
            f"Błąd operacyjny SQLite. Sprawdź czy plik istnieje i zawiera wymagane tabele. "
            f"Ścieżka: {DATABASE_PATH}"
        ) from e

    except sqlite3.DatabaseError as e:
        raise sqlite3.DatabaseError(
            f"Błąd bazy danych podczas wczytywania danych z: {DATABASE_PATH}"
        ) from e

    except Exception as e:
        raise RuntimeError(
            "Nieoczekiwany błąd podczas wczytywania danych z bazy SQLite"
        ) from e