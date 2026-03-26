import pandas as pd
from project.config import PROCESSED_PATH, TABLES_PATH, PLOTS_PATH, SUB_DIRS


def create_directories():
    """
    Tworzy wszystkie wymagane katalogi projektu, jeśli nie istnieją:
    - PROCESSED_PATH
    - TABLES_PATH
    - PLOTS_PATH
    """
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    TABLES_PATH.mkdir(parents=True, exist_ok=True)
    PLOTS_PATH.mkdir(parents=True, exist_ok=True)


def get_plot_folder(folder_name: str):
    """
    Zwraca ścieżkę do folderu wykresów i tworzy go jeśli nie istnieje.

    Parametry
    ----------
    folder_name : str
        Nazwa podfolderu (np. 'gender_comparison').

    Zwraca
    -------
    Path
        Ścieżka do folderu.
    """

    folder = PLOTS_PATH / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def create_subdirs():
    """
    Tworzy wszystkie podfoldery w katalogach PLOTS_PATH i TABLES_PATH
    na potrzeby różnych analiz.
    Zwraca słownik z listą utworzonych folderów.
    """
    created_folders = {"plots": [], "tables": []}

    for parent in [(PLOTS_PATH, "plots"), (TABLES_PATH, "tables")]:
        base_path, key = parent
        for sd in SUB_DIRS:
            folder = base_path / sd
            folder.mkdir(parents=True, exist_ok=True)
            created_folders[key].append(folder)

    return created_folders


def save_processed(df: pd.DataFrame, filename: str):
    """
    Zapisuje przetworzony DataFrame do katalogu PROCESSED_PATH jako CSV.

    Parametry
    ----------
    df : pd.DataFrame
        Dane do zapisania.
    filename : str
        Nazwa pliku (np. "df_joined.csv").
    """
    path = PROCESSED_PATH / filename
    df.to_csv(path, index=False)


def save_table(df: pd.DataFrame, subdir:str, filename: str):
    """
    Zapisuje DataFrame ze statystyk lub tabel do katalogu TABLES_PATH jako CSV.

    Parametry
    ----------
    df : pd.DataFrame
        Dane do zapisania.
    filename : str
        Nazwa pliku (np. "stats_input.csv").
    """
    if subdir is None:
        path = TABLES_PATH / filename
        df.to_csv(path, index=True)
    else:

        path = TABLES_PATH / subdir / filename
        df.to_csv(path, index=True)


def save_plot(fig, subdir:str, filename: str):
    """
    Zapisuje wykres Plotly do katalogu PLOTS_PATH w formacie HTML.

    Parametry
    ----------
    fig : plotly.graph_objects.Figure
        Obiekt wykresu Plotly.
    filename : str
        Nazwa pliku, np. "feature_bar_mean_vs_median.html".
    """
    path = PLOTS_PATH / subdir / filename
    fig.write_html(path)
