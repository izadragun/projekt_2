import pandas as pd
from project.config import (
    PATIENT_ID_COLUMN,
    VISIT_ID_COLUMN,
    TIME_COLUMN,
    STATIC_COLUMNS,
    AGGREGATION_METHODS
)


def join_tables(patients: pd.DataFrame,
                visits: pd.DataFrame,
                measurements: pd.DataFrame) -> pd.DataFrame:
    """
    Łączy tabele pacjentów, wizyt oraz pomiarów w jeden DataFrame.

    Operacja odbywa się w dwóch krokach:
    1. Połączenie tabel `visits` i `measurements` na podstawie
       identyfikatora pacjenta oraz daty pomiaru.
    2. Dołączenie danych demograficznych pacjenta z tabeli `patients`.

    Przed połączeniem kolumny z datami są konwertowane do typu datetime.

    Parametry
    ----------
    patients : pd.DataFrame
        Tabela zawierająca dane pacjentów.

    visits : pd.DataFrame
        Tabela wizyt pacjentów.

    measurements : pd.DataFrame
        Tabela pomiarów biomarkerów.

    Zwraca
    -------
    pd.DataFrame
        DataFrame zawierający połączone dane wizyt, pomiarów oraz
        informacje o pacjentach.
    """
    visits = visits.copy()
    measurements = measurements.copy()

    # zmiana formatu dat na datetime
    visits[TIME_COLUMN] = pd.to_datetime(visits[TIME_COLUMN])
    measurements["measured_at"] = pd.to_datetime(measurements["measured_at"])

    # łączenie visits z measurements po patient_id + data
    df = visits.merge(
        measurements,
        left_on=[PATIENT_ID_COLUMN, TIME_COLUMN],
        right_on=[PATIENT_ID_COLUMN, "measured_at"],
        how="inner"
    )

    # dołączenie danych pacjenta
    df = df.merge(
        patients,
        on=PATIENT_ID_COLUMN,
        how="inner"
    )

    return df


def create_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tworzy macierz cech (feature matrix) na poziomie wizyty.

    Funkcja przekształca dane do formatu szerokiego (wide format),
    gdzie każdy typ pomiaru (`kind`) staje się osobną kolumną,
    a wartości pomiarów są przechowywane w kolumnach biomarkerów.

    Indeksem macierzy są informacje identyfikujące wizytę oraz
    podstawowe dane pacjenta.

    Parametry
    ----------
    df : pd.DataFrame
        DataFrame zawierający dane połączone z tabel
        pacjentów, wizyt oraz pomiarów.

    Zwraca
    -------
    pd.DataFrame
        Macierz cech, w której każdy wiersz odpowiada jednej wizycie,
        a kolumny reprezentują poszczególne biomarkery.
    """

    index_cols = [
        PATIENT_ID_COLUMN,
        VISIT_ID_COLUMN,
        TIME_COLUMN,
        *STATIC_COLUMNS
    ]

    matrix = df.pivot(
        index=index_cols,
        columns="kind",
        values="value"
    )

    matrix.columns.name = None
    matrix = matrix.reset_index()

    return matrix


def aggregate(
    df: pd.DataFrame,
    method: str
) -> pd.DataFrame:
    """
    Agreguje dane biomarkerów na poziomie pacjenta.

    Funkcja oblicza statystykę (średnią lub medianę) dla wszystkich
    kolumn numerycznych związanych z biomarkerami, grupując dane
    według identyfikatora pacjenta.

    Kolumny identyfikacyjne oraz kolumny statyczne nie są agregowane.
    Dane statyczne pacjenta są pobierane z pierwszego wystąpienia
    w grupie.

    Parametry
    ----------
    df : pd.DataFrame
        DataFrame zawierający dane wizyt i biomarkerów.

    method : str
        Metoda agregacji. Dozwolone wartości:
        - "mean" – średnia
        - "median" – mediana

    Zwraca
    -------
    pd.DataFrame
        DataFrame na poziomie pacjenta zawierający dane statyczne
        oraz zagregowane wartości biomarkerów.

    Wyjątki
    -------
    ValueError
        Jeśli `method` nie jest jedną z dozwolonych wartości.
    """

    if method not in AGGREGATION_METHODS:
        raise ValueError(f"method must be one of {AGGREGATION_METHODS}")

    # kolumny numeryczne
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # usuń ID i kolumny statyczne
    numeric_cols = [
        col for col in numeric_cols
        if col not in (
            [PATIENT_ID_COLUMN, VISIT_ID_COLUMN] +
            STATIC_COLUMNS
        )
    ]

    # agregacja biomarkerów
    df_numeric = (
        df.groupby(PATIENT_ID_COLUMN)[numeric_cols]
        .agg(method)
    )

    # dane statyczne
    df_static = (
        df.groupby(PATIENT_ID_COLUMN)[STATIC_COLUMNS]
        .first()
    )

    # join
    df_patient = df_static.join(df_numeric)

    return df_patient.reset_index()

