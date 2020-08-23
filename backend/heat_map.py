from urllib.request import urlopen
import json
import pandas as pd
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("../data/total_week_cases.csv", 
                        dtype={"fips": str})


def generate_map(df):
    fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                            color_continuous_scale="reds",
                            range_color=(0, 100),
                            scope="usa",
                            labels={'cases':'number of cases'},
                            title='Heat Map of Daily Cases Across U.S. Counties'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plotly.offline.plot(fig, filename='../static/map_week_cases.html')

if __name__ == "__main__":
    generate_map(df)