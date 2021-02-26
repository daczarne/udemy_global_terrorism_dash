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
						)
            # Title for second dropdown
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


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
