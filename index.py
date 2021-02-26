import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from numpy.lib.twodim_base import triu_indices_from
import plotly.graph_objs as go
import pandas as pd

# Load data
terr2 = pd.read_csv("data/global_terrorism.csv")

# Instanciate the app
app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])

# Build layout
app.layout = html.Div(
  [
    # (First Row): Title
    html.Div(
      [
        # (Column 1): Title
        html.Div(
          [
            html.Div(
              [
                # Title
                html.H3(
                  children = "Global terrorism database",
                  style = {
                    "margin-bottom": "0px",
                    "color": "white"
                  }
                ),
                # Subtitle
                html.H5(
                  children = "1970 - 2017",
                  style = {
                    "margin-top": "0px",
                    "color": "white"
                  }
                )
              ]
            )
          ],
          className = "six column",
          id = "title"
        )
      ],
      id = "header",
      className = "row flex-display",
      style = {
        "margin-bottom": "25px"
      }
    ),
    # (Second Row): Map
    
    # (Third Row): Plots
    html.Div(
      [
        # (Column one) User inputs
        html.Div(
          [
            # Title for first dropdown
            html.P(
              children = "Select Region",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # First dropdown
            dcc.Dropdown(
							id = "w_countries",
							multi = False,
							searchable = True,
							value = "South Asia",
							placeholder = "Select Region",
							options = [{"label": c, "value": c} for c in (terr2["region_txt"].unique())],
							className = "dcc_compon"
						),
            # Title for second dropdown
            html.P(
              children = "Select Country",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # First dropdown
            dcc.Dropdown(
							id = "w_countries1",
							multi = False,
							searchable = True,
							placeholder = "Select Country",
							options = [],
							className = "dcc_compon"
						),
            # Title for range slider
            html.P(
              children = "Select Years",
              className = "fix_label",
              style = {
                "color": "white"
              }
            ),
            # Range slider
            dcc.RangeSlider(
							id = "select_years",
              min = terr2["iyear"].min(),
              max = terr2["iyear"].max(),
              dots = False,
              value = [2010, 2017]
						)
          ],
          className = "create_containter three columns"
        ),
        # (Column two) Bars and line chart
        html.Div(
          [
            dcc.Graph(
              id = "bar_chart",
              config = {
                "displayModeBar": "hover"
              }
            )
          ],
          className = "create_container six columns"
        )
      ],
      className = "row flex-display"
    )
  ],
  id = "mainContainer",
	style = {
		"display": "flex",
		"flex-direction": "column"
	}
)


# Update second dropdown
@app.callback(
  Output(
    component_id = "w_countries1",
    component_property = "options"
  ),
  Output(
    component_id = "w_countries1",
    component_property = "value"
  ),
  Input(
    component_id = "w_countries",
    component_property = "value"
  )
)
def update_country(w_countries):
  # Filter the region
  terr3 = terr2[terr2["region_txt"] == w_countries]
  # Build list of countries
  list_of_countries = [{"label": i, "value": i} for i in terr3["country_txt"].unique()]
  # Return list and value
  return list_of_countries, list_of_countries[0]["value"]


# Update line and bars char
@app.callback(
  Output(
    component_id = "bar_chart",
    component_property = "figure"
  ),
  Input(
    component_id = "w_countries",
    component_property = "value"
  ),
  Input(
    component_id = "w_countries1",
    component_property = "value"
  ),
  Input(
    component_id = "select_years",
    component_property = "value"
  )
)
def update_country(w_countries, w_countries1, selected_years):
  terr2[["nkill", "nwound", "attacktype1"]] = terr2[["nkill", "nwound", "attacktype1"]].fillna(0)
  terr5 = terr2.groupby(["region_txt", "country_txt", "iyear"])[["nkill", "nwound", "attacktype1"]].sum().reset_index()
  # Filter the region
  terr6 = terr5[
    (terr5["region_txt"] == w_countries) &
    (terr5["country_txt"] == w_countries1) &
    (terr5["iyear"] >= selected_years[0]) &
    (terr5["iyear"] <= selected_years[1])
  ]
  # Build fig
  fig = {
    "data": [
      # Deaths
      go.Scatter(
        x = terr6["iyear"],
        y = terr6["nkill"],
        mode = "markers+lines",
        name = "Deaths",
        line = dict(
          shape = "spline",
          smoothing = 1.3,
          width = 3,
          color = "#ff00ff"
        ),
        marker = dict(
          color = "white",
          size = 10,
          symbol = "circle",
          line = dict(
            color = "#ff00ff",
            width = 2
          )
        ),
        hoverinfo = "text",
        hovertext = 
        "<b>Region:</b> " + terr6["region_txt"].astype(str) + "<br>" +
        "<b>Country:</b> " + terr6["country_txt"].astype(str) + "<br>" +
        "<b>Year:</b> " + terr6["iyear"].astype(str) + "<br>" + 
        "<b>Death:</b> " + terr6["nkill"].astype(str) + "<br>" + 
        "<extra></extra>"
      ),
      # Wounded
      go.Bar(
        x = terr6["iyear"],
        y = terr6["nwound"],
        text = terr6["nwound"],
        texttemplate = "%{text:,.0f}",
        textposition = "auto",
        name = "Injured",
        marker = dict(
          color = "#9c0c38",
        ),
        hoverinfo = "text",
        hovertext = 
        "<b>Region:</b> " + terr6["region_txt"].astype(str) + "<br>" +
        "<b>Country:</b> " + terr6["country_txt"].astype(str) + "<br>" +
        "<b>Year:</b> " + terr6["iyear"].astype(str) + "<br>" + 
        "<b>Injured:</b> " + terr6["nwound"].astype(str) + "<br>" + 
        "<extra></extra>"
      ),
      # Attack
      go.Bar(
        x = terr6["iyear"],
        y = terr6["attacktype1"],
        text = terr6["attacktype1"],
        texttemplate = "%{text:,.0f}",
        textposition = "auto",
        name = "Attack",
        marker = dict(
          color = "orange",
        ),
        hoverinfo = "text",
        hovertext = 
        "<b>Region:</b> " + terr6["region_txt"].astype(str) + "<br>" +
        "<b>Country:</b> " + terr6["country_txt"].astype(str) + "<br>" +
        "<b>Year:</b> " + terr6["iyear"].astype(str) + "<br>" + 
        "<b>Attack:</b> " + terr6["attacktype1"].astype(str) + "<br>" + 
        "<extra></extra>"
      )
    ],
    "layout": go.Layout(
      title = {
        "text": "Deaths, Injured, Attack in " + w_countries1 + "<br>" +
                " - ".join([str(y) for y in selected_years]) + "<br>",
        "x": 0.5,
        "y": 0.93,
        "xanchor": "center",
        "yanchor": "top"
      },
      titlefont = {
        "color": "white",
        "size": 20
      },
      font = {
        "family": "sans-serif",
        "color": "white",
        "size": 12
      },
      hovermode = "closest",
      paper_bgcolor = "#010915",
      plot_bgcolor = "#010915",
      legend = {
        "orientation": "h",
        "bgcolor": "#010915",
        "xanchor": "center",
        "x": 0.5,
        "y": -0.7
      },
      margin = {
        "r": 0
      },
      xaxis = {
        "title": "<b>Year</b>",
        "color": "white",
        "showline": True,
        "showgrid": True,
        "showticklabels": True,
        "linecolor": "white",
        "linewidth": 1,
        "ticks": "outside",
        "tick0": 0,
        "dtick": 1,
        "tickfont": {
          "family": "Aerial",
          "color": "white",
          "size": 12
        }
      },
      yaxis = {
        "title": "<b>Deaths, Injured, Attack</b>",
        "color": "white",
        "showline": True,
        "showgrid": True,
        "showticklabels": True,
        "linecolor": "white",
        "linewidth": 1,
        "ticks": "outside",
        "tickfont": {
          "family": "Aerial",
          "color": "white",
          "size": 12
        }
      },
      barmode = "stack"
    )
  }
  # Return list and value
  return fig


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
