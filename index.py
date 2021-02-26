import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
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


# Build callbacks
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


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
