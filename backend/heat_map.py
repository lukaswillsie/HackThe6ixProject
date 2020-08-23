from urllib.request import urlopen
import json
import pandas as pd
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", 
                        dtype={"fips": str})


def generate_map(df):
    fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope="usa",
                            labels={'unemp':'unemployment rate'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plotly.offline.plot(fig, filename='map.html')

if __name__ == "__main__":
    generate_map(df)