import marimo

__generated_with = "0.13.10"
app = marimo.App(width="full")


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

    This is not exact science, because there are too many variables at stake.

    ## TODO

    - compress the two charts into a single one, so it's easier to read at a glance
    """
    )
    return


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    return go, pd, px


@app.cell
def _():
    dashboard_data = {
        "product": {
            "authentication": 2,
            "aesthetics": 3,
            "ML engineering UX": 2,
            "notebooks UX": 11,
            "git": 2
        },
        "distribution": {
            "educational content": 0,
            "presence on socials": 1,
            "open source contributions": 2,
            "irl events": 1,
        },
        "revenue": {
            "subscriptions": 0,
            "usage": 0
        },
        "partners": {
            "Voltalia": 4,
            "Colibri": 1,
            "Serena": 1
        },
        "team": {
            "members": 6,
            "advisors": 2
        },
        "investment": {
            "pitches": 5,
            "accelerators": 2,
            "signed": 0
        }
    }
    return (dashboard_data,)


@app.cell
def _(dashboard_data, go):
    category_sums = {}
    for category, items in dashboard_data.items():
        category_sums[category] = sum(items.values())

    # Create pie chart
    fig_piechart = go.Figure(data=[go.Pie(
        labels=list(category_sums.keys()),
        values=list(category_sums.values()),
        hole=.3,
        textinfo='label+value'
    )])

    fig_piechart.update_layout(
        title_text="Enverge Overview",
        height=600,
        width=800
    )

    fig_piechart
    return


@app.cell
def _(dashboard_data, pd):
    areas = []
    for section_key, section_value in dashboard_data.items():
        for area_key, area_value in section_value.items():
            areas.append({"Section": section_key, "Area": area_key, "Value": area_value})
    areas_df = pd.DataFrame(areas)
    return (areas_df,)


@app.cell
def _(areas_df, go, px):
    unique_sections = areas_df['Section'].unique()
    colors = px.colors.qualitative.Plotly

    fig = go.Figure()
    for i, section in enumerate(unique_sections):
        section_df = areas_df[areas_df['Section'] == section]
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
        title='Value by Area and Section',
        xaxis_tickangle=45,
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
    )

    fig
    return


if __name__ == "__main__":
    app.run()
