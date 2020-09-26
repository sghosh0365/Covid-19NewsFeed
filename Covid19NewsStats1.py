import requests
import json
import datetime
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.offline as offline
from plotly.offline import plot_mpl


def generate_maps_1():
    try:
        resp = requests.get('https://api.covid19api.com/summary')
        resp_json = resp.json()
        df = pd.DataFrame(resp_json['Countries'])
        data = dict(
            type='choropleth',
            colorscale='Reds',
            autocolorscale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            locations=df['Country'],
            locationmode="country names",
            z=df['NewConfirmed'],
            text=df['Country'],
            colorbar={'title': 'New confirmed cases'},
        )

        layout = dict(
            geo=dict(showframe=False, projection={'type': 'mercator'}) 
        )
        choromap = go.Figure({'data': [data], 'layout': layout})
        choromap.write_image("covid-19map.png")
        print('Completed execution of Covid19NewsStats-1.py')
    except Exception as ex:
        print(f'{ex}')
