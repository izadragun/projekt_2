import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from project.config import (
    FEATURE_COLUMNS,
    PLOTS_PATH
)


def plot_histogram_comparison(
        df_mean: pd.DataFrame,
        df_median: pd.DataFrame,
        feature: str
):
    """
    Tworzy histogram porównujący rozkład wartości biomarkera
    w danych po agregacji mean i median.

    Parametry
    ----------
    df_mean : pd.DataFrame
        Dane po agregacji mean.
    df_median : pd.DataFrame
        Dane po agregacji median.
    feature : str
        Nazwa biomarkera do wizualizacji.

    Zapisuje
    --------
    Wykres HTML w katalogu PLOTS_PATH o nazwie '{feature}_hist_mean_vs_median.html'.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df_mean[feature],
            name="Mean aggregation",
            opacity=0.6
        )
    )

    fig.add_trace(
        go.Histogram(
            x=df_median[feature],
            name="Median aggregation",
            opacity=0.7
        )
    )

    fig.update_layout(
        title=f"{feature}: porównanie rozkładu wartości po agregacji",
        xaxis_title=feature,
        yaxis_title="Count",
        barmode="overlay",
        template="plotly_white"
    )

    fig.write_html(PLOTS_PATH / f"{feature}_hist_mean_vs_median.html")


def plot_box_mean_vs_median(
        df_mean: pd.DataFrame,
        df_median: pd.DataFrame,
        feature: str
):
    """
    Tworzy boxplot porównujący rozkład wartości biomarkera
    po agregacji mean oraz median.

    Parametry
    ----------
    df_mean : pd.DataFrame
        Dane po agregacji mean (jedna wartość biomarkera na pacjenta).
    df_median : pd.DataFrame
        Dane po agregacji median.
    feature : str
        Nazwa biomarkera do wizualizacji.

    Zapisuje
    --------
    Wykres HTML w katalogu PLOTS_PATH.
    """

    df_plot = pd.DataFrame({
        "value": pd.concat([df_mean[feature], df_median[feature]]),
        "aggregation": (
                ["mean"] * len(df_mean) +
                ["median"] * len(df_median)
        )
    })

    fig = px.box(
        df_plot,
        x="aggregation",
        y="value",
        title=f"{feature}: distribution after aggregation",
        template="plotly_white"
    )

    fig.write_html(
        PLOTS_PATH / f"{feature}_box_mean_vs_median.html"
    )


def plot_scatter_mean_vs_median(
        df_mean: pd.DataFrame,
        df_median: pd.DataFrame,
        feature: str
):
    """
    Tworzy scatter plot porównujący wartości biomarkera
    dla każdego pacjenta po agregacji mean vs median.

    Parametry
    ----------
    df_mean : pd.DataFrame
        Dane po agregacji mean.
    df_median : pd.DataFrame
        Dane po agregacji median.
    feature : str
        Nazwa biomarkera do wizualizacji.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_mean[feature],
            y=df_median[feature],
            mode="markers",
            name="patients",
            hovertemplate=(
                "MeanAgg: %{x:.3f}<br>"
                "MedianAgg: %{y:.3f}<extra></extra>"
            )
        )
    )

    # linia idealnej zgodności
    fig.add_shape(
        type="line",
        x0=df_mean[feature].min(),
        y0=df_mean[feature].min(),
        x1=df_mean[feature].max(),
        y1=df_mean[feature].max(),
        line=dict(dash="dash")
    )

    fig.update_layout(
        title=f"{feature}: mean vs median aggregation",
        xaxis_title="Mean aggregation",
        yaxis_title="Median aggregation",
        template="plotly_white"
    )

    fig.write_html(
        PLOTS_PATH / f"{feature}_scatter_mean_vs_median.html"
    )


def plot_difference_histogram(
        df_mean: pd.DataFrame,
        df_median: pd.DataFrame,
        feature: str
):
    """
    Tworzy histogram różnicy wartości biomarkera
    pomiędzy agregacją mean i median.

    Parametry
    ----------
    df_mean : pd.DataFrame
        Dane po agregacji mean.
    df_median : pd.DataFrame
        Dane po agregacji median.
    feature : str
        Nazwa biomarkera.
    """

    diff = df_mean[feature] - df_median[feature]

    fig = px.histogram(
        diff,
        nbins=30,
        title=f"{feature}: difference (meanAgg - medianAgg)",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="Difference",
        yaxis_title="Count"
    )

    fig.write_html(
        PLOTS_PATH / f"{feature}_difference_histogram.html"
    )


def generate_all_plots(
        df_mean: pd.DataFrame,
        df_median: pd.DataFrame
):
    """
    Generuje komplet wykresów porównujących agregację
    mean i median dla wszystkich biomarkerów.

    Parametry
    ----------
    df_mean : pd.DataFrame
        Dane po agregacji mean.
    df_median : pd.DataFrame
        Dane po agregacji median.
    """

    for feature in FEATURE_COLUMNS:
        plot_box_mean_vs_median(
            df_mean,
            df_median,
            feature
        )

        plot_scatter_mean_vs_median(
            df_mean,
            df_median,
            feature
        )

        plot_difference_histogram(
            df_mean,
            df_median,
            feature
        )

        plot_histogram_comparison(df_mean, df_median, feature)

