import pandas as pd


def statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Oblicza statystyki opisowe dla biomarkerów w DataFrame.

    Funkcja wybiera kolumny biomarkerów (z wyłączeniem kolumn
    identyfikacyjnych i demograficznych), a następnie oblicza
    podstawowe statystyki opisowe oraz dodatkowe informacje
    o brakujących danych.

    Parametry
    ----------
    df : pd.DataFrame
        DataFrame zawierający dane pacjentów, wizyt oraz biomarkerów.

    Zwraca
    -------
    pd.DataFrame
        DataFrame zawierający statystyki opisowe dla biomarkerów,
        w tym m.in. średnią, medianę, odchylenie standardowe,
        zakres wartości oraz informacje o brakach danych.
    """

    exclude_cols = [
        'patient_id',
        'visit_id',
        'visit_date',
        'age',
        'gender',
        'class'
    ]

    # wybrane kolumny numeryczne
    biomarker_cols = [col for col in df.columns if col not in exclude_cols]

    # podstawowe statystyki opisowe
    stats = df[biomarker_cols].describe()
    stats = stats.rename(index={"50%": "median"})
    # dodatkowe statystyki
    stats.loc['missing_count'] = df[biomarker_cols].isna().sum()
    stats.loc['missing_percent'] = df[biomarker_cols].isna().mean() * 100
    stats.loc['total_rows'] = len(df)

    # range (maksimum - minimum)
    stats.loc['range'] = stats.loc['max'] - stats.loc['min']

    return stats


def compare_statistics(
        stats_input: pd.DataFrame,
        stats_mean: pd.DataFrame,
        stats_median: pd.DataFrame
) -> pd.DataFrame:
    """
    Tworzy tabelę porównawczą statystyk dla danych wejściowych
    oraz danych po agregacji metodami mean i median.

    Funkcja wybiera wybrane statystyki opisowe (mean, std, median,
    missing_percent) z trzech zestawów danych, a następnie łączy je
    w jedną tabelę. Dodatkowo obliczana jest różnica pomiędzy
    agregacją mean i median dla średniej wartości biomarkerów.

    Parametry
    ----------
    stats_input : pd.DataFrame
        DataFrame zawierający statystyki opisowe dla danych
        przed agregacją.

    stats_mean : pd.DataFrame
        DataFrame zawierający statystyki opisowe dla danych
        po agregacji metodą mean.

    stats_median : pd.DataFrame
        DataFrame zawierający statystyki opisowe dla danych
        po agregacji metodą median.

    Zwraca
    -------
    pd.DataFrame
        DataFrame zawierający porównanie statystyk dla każdej cechy
        (biomarkera) oraz różnice pomiędzy metodami agregacji.
        Tabela jest posortowana malejąco według procentowej różnicy
        między agregacjami.
    """

    rows_to_keep = [
        "mean",
        "std",
        "median",
        "missing_percent"
    ]

    input_stats = stats_input.loc[rows_to_keep].T.add_prefix("input_")
    mean_stats = stats_mean.loc[rows_to_keep].T.add_prefix("meanAgg_")
    median_stats = stats_median.loc[rows_to_keep].T.add_prefix("medianAgg_")

    comparison_df = pd.concat(
        [input_stats, mean_stats, median_stats],
        axis=1
    ).reset_index()

    comparison_df = comparison_df.rename(columns={"index": "feature"})

    # różnica między agregacjami
    comparison_df["difference_between_aggregations"] = (
            comparison_df["meanAgg_mean"] -
            comparison_df["medianAgg_mean"]
    )

    # różnica procentowa
    comparison_df["difference_percent_between_aggregations"] = (comparison_df["difference_between_aggregations"] /
                                                                comparison_df["medianAgg_mean"]) * 100

    return comparison_df.sort_values(
        "difference_percent_between_aggregations",
        ascending=False
    )
