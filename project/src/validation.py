import pandas as pd

from project.config import (
    PATIENT_ID_COLUMN,
    VISIT_ID_COLUMN,
    TIME_COLUMN
)


def validate_input_data(
        patients: pd.DataFrame,
        visits: pd.DataFrame,
        measurements: pd.DataFrame
):
    """
    Przeprowadza pełną walidację danych wejściowych
    przed łączeniem tabel.

    Sprawdzane są:
    - obecność wymaganych kolumn
    - duplikaty identyfikatorów
    - spójność relacji między tabelami

    Parametry
    ----------
    patients : pd.DataFrame
        Tabela pacjentów.

    visits : pd.DataFrame
        Tabela wizyt.

    measurements : pd.DataFrame
        Tabela pomiarów biomarkerów.

    Raises
    ------
    ValueError
        Jeśli wykryto problem ze strukturą danych.
    """

    _validate_patients(patients)
    _validate_visits(visits)
    _validate_measurements(measurements)
    # nowa walidacja relacji
    _validate_relationships(
        patients,
        visits,
        measurements
    )


def _validate_patients(df: pd.DataFrame):
    """
    Sprawdza poprawność tabeli patients.
    """

    required_cols = [PATIENT_ID_COLUMN]

    _check_columns(df, required_cols)

    if df[PATIENT_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Tabela patients zawiera zduplikowane patient_id."
        )


def _validate_visits(df: pd.DataFrame):
    """
    Sprawdza poprawność tabeli visits.
    """

    required_cols = [
        PATIENT_ID_COLUMN,
        VISIT_ID_COLUMN,
        TIME_COLUMN
    ]

    _check_columns(df, required_cols)

    duplicates = df.duplicated(
        subset=[PATIENT_ID_COLUMN, VISIT_ID_COLUMN]
    )

    if duplicates.any():
        n_duplicates = duplicates.sum()

        raise ValueError(
            f"Tabela visits zawiera {n_duplicates} "
            f"duplikatów wizyt (patient_id + visit_id)."
        )


def _validate_measurements(df: pd.DataFrame):
    """
    Sprawdza poprawność tabeli measurements.
    """

    required_cols = [
        PATIENT_ID_COLUMN,
        "measured_at",
        "kind",
        "value"
    ]

    _check_columns(df, required_cols)

    if not pd.api.types.is_numeric_dtype(df["value"]):
        raise ValueError(
            "Kolumna 'value' w measurements musi być numeryczna."
        )


def _validate_relationships(
        patients: pd.DataFrame,
        visits: pd.DataFrame,
        measurements: pd.DataFrame
):
    """
    Sprawdza spójność relacji między tabelami.

    Kontroluje czy wszystkie patient_id z visits i measurements
    istnieją w tabeli patients.

    Raises
    ------
    ValueError
        Jeśli wykryto niespójność relacji.
    """

    patient_ids = set(patients[PATIENT_ID_COLUMN])

    # visits → patients
    visits_ids = set(visits[PATIENT_ID_COLUMN])
    missing_visits = visits_ids - patient_ids

    if missing_visits:
        raise ValueError(
            f"W tabeli visits występują patient_id "
            f"nieobecne w patients: {list(missing_visits)[:5]}"
        )

    # measurements → patients
    measurement_ids = set(measurements[PATIENT_ID_COLUMN])
    missing_measurements = measurement_ids - patient_ids

    if missing_measurements:
        raise ValueError(
            f"W tabeli measurements występują patient_id "
            f"nieobecne w patients: {list(missing_measurements)[:5]}"
        )


def _check_columns(df: pd.DataFrame, required_cols: list):
    """
    Sprawdza czy DataFrame zawiera wymagane kolumny.
    """

    missing = set(required_cols) - set(df.columns)

    if missing:
        raise ValueError(
            f"Brak wymaganych kolumn: {missing}"
        )
