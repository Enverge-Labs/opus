import marimo

__generated_with = "0.14.7"
app = marimo.App(width="full", layout_file="layouts/app.grid.json")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Enverge Overview
    How can we keep ourselves focused and accountable if we don't know what are we tracking?

    This is not exact science, because there are too many variables at play.

    **Every week we each get 20 units to update**
    """
    )
    return


@app.cell
def _():
    import datetime
    import json
    from pathlib import Path

    import pandas as pd

    import plotly.express as px
    import plotly.graph_objects as go

    return Path, datetime, go, json, pd, px


@app.cell
def _(datetime):
    CURRENT_WEEK = 26
    CURRENT_CALENDAR_WEEK = datetime.datetime.today().isocalendar().week
    return CURRENT_CALENDAR_WEEK, CURRENT_WEEK


@app.cell
def _(CURRENT_CALENDAR_WEEK, CURRENT_WEEK, mo):
    mo.md(
        rf"""
    # Current calendar week {CURRENT_CALENDAR_WEEK}.
    # Current week {CURRENT_WEEK} in data.
    """
    )
    return


@app.cell
def _(Path, json, pd):
    # Data structure: Section -> Area -> Value
    def get_weekly_data(current_week: int) -> pd.DataFrame:
        weekly_data = []

        data_path = Path(f"./dashboard_state_week_{current_week}.json")
        dashboard_data = json.loads(data_path.read_text())

        for section_key, section_value in dashboard_data.items():
            for area_key, area_value in section_value.items():
                weekly_data.append({"Section": section_key, "Area": area_key, "Value": area_value})
        return weekly_data
    return (get_weekly_data,)


@app.cell
def _(CURRENT_WEEK, get_weekly_data, pd):
    weekly_df = pd.DataFrame(get_weekly_data(CURRENT_WEEK))
    return (weekly_df,)


@app.cell
def _(CURRENT_CALENDAR_WEEK, get_weekly_data, pd):
    week_when_data_started = 23
    week_range = range(week_when_data_started, CURRENT_CALENDAR_WEEK+1)

    all_dfs = [
        pd.DataFrame(get_weekly_data(w))
        for w in week_range
    ]
    all_data = pd.concat(all_dfs, ignore_index=True)
    areas_sums_df = all_data.groupby(["Section", "Area"])["Value"].sum().reset_index()
    return (areas_sums_df,)


@app.cell
def _(go):
    def generate_sums_pie(df, title: str) -> go.Figure:
        section_totals = df.groupby("Section")["Value"].sum().reset_index()
        fig_piechart = go.Figure(data=[go.Pie(
            labels=section_totals["Section"],
            values=section_totals["Value"],
            textinfo='label+percent',
            hole=.3,
            textposition='auto'
        )])

        fig_piechart.update_layout(
            title_text=title,
            height=500,
            width=500
        )
        return fig_piechart
    return (generate_sums_pie,)


@app.cell
def _(generate_sums_pie, weekly_df):
    generate_sums_pie(weekly_df, "Weekly Sums")
    return


@app.cell
def _(areas_sums_df, generate_sums_pie):
    generate_sums_pie(areas_sums_df, "Overall Sums")
    return


@app.cell
def _(go, px):
    def generate_all_areas(df, title: str) -> go.Figure:
        unique_sections =  sorted(df['Section'].unique())
        colors = px.colors.qualitative.Plotly
    
        fig = go.Figure()
        for i, section in enumerate(unique_sections):
            section_df = df[df['Section'] == section]
            fig.add_trace(go.Bar(
                x=section_df['Area'],
                y=section_df['Value'],
                name=section,
                marker_color=colors[i % len(colors)]
            ))
    
        fig.update_layout(
            barmode='group',
            xaxis_title='Section + Area',
            yaxis_title='Attention + Effort',
            yaxis=dict(range=[0, 50]),
            title=title,
            xaxis_tickangle=45,
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
        )
        return fig
    return (generate_all_areas,)


@app.cell
def _(generate_all_areas, weekly_df):
    generate_all_areas(weekly_df, "Weekly - Value by Area and Section")
    return


@app.cell
def _(areas_sums_df, generate_all_areas):
    generate_all_areas(areas_sums_df, "Overall - Value by Area and Section")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## TODO

    - compress the two charts into a single one, so it's easier to read at a glance
    - TBD
    """
    )
    return


if __name__ == "__main__":
    app.run()
