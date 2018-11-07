import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime as dt
pyo_config={'showLink': False, 'displaylogo':False, 'modeBarButtonsToRemove':['sendDataToCloud']}

# read source data
df = pd.read_csv('data/normalized_data.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# add custm columns
df['year'] = df.index.year
df['month'] = df.index.month
df['rainy_day'] = np.where(df['rain_fall'] > 0, True, False)
df['sunny_day'] = np.where(df['sunshine_duration'] > 4, True, False)
df['day_with_snow'] = np.where(df['snow_height'] > 0, True, False)

# data agregation
df_by_year_sum = df.groupby(df.index.year).sum() / 12
df_by_year_mean = df.groupby(df.index.year).mean()
df_by_month_sum = df.groupby(df.index.month).sum() / len(df.index.year.unique())
df_by_month_mean = df.groupby(df.index.month).mean()
df_by_year_month_mean = df.groupby(['year','month']).mean().reset_index()

# initiate dashboard app
app = dash.Dash()
server = app.server
app.title = 'Brno Weather Trend Analyses'
# define chart
data = [go.Scatter(
                x=df_by_month_sum.index,
                y=df_by_month_sum['rainy_day'],
                mode='markers',
                name='average rainfall (mm)',
                marker=dict(size=( df_by_month_sum['rain_fall'] / df_by_month_sum['rainy_day'])*8),
                text =  df_by_month_sum['rain_fall'] / df_by_month_sum['rainy_day']
                ),
        go.Scatter(
                x=df_by_month_sum.index,
                y=df_by_month_sum['sunny_day'],
                mode='markers',
                name='average sunshine duration in day (hours)',
                text=df_by_month_sum['sunshine_duration'] / df_by_month_sum['sunny_day'],
                #marker=dict(size=df_by_month_mean['sunshine_duration']*6)
                marker=dict(size=(df_by_month_sum['sunshine_duration'] / df_by_month_sum['sunny_day'])*4)
                ),
        go.Scatter(x=df_by_month_mean.index,
                y=df_by_month_mean['temperature_MAX'],
                mode='lines',
                name = 'max daily temperature',
                yaxis='y2',
                marker=dict(color='red')),
        go.Scatter(x=df_by_month_mean.index,
                y=df_by_month_mean['temperature_AVG'],
                mode='lines',
                name = 'average daily temperature',
                yaxis='y2',
                marker=dict(color='green')),
        go.Scatter(x=df_by_month_mean.index,
                y=df_by_month_mean['temperature_MIN'],
                mode='lines',
                name = 'min daily temperature',
                yaxis='y2',
                marker=dict(color='blue'))
       ]

layout = go.Layout(
    title='Rainfall, Sunshine and Temperature Trends during the Year',
    xaxis=dict(
        title='month',
        dtick=1),
    yaxis=dict(
        title='average no. of rainy  / sunny days',
        zeroline=False,
        range=[0,30]
    ),
    yaxis2=dict(
        title='temperature (C)',
        overlaying='y',
        side='right',
        zeroline=False
    )
)
# build app layout
app.layout = html.Div([
        html.H1('Brno Weather Trend Analyses'),
        html.P('This website explore more than 50 years of historical weather data collected by the Czech Hydrometheological Institute (www.chmi.cz) in Brno - Turany.'),
        html.P('I used this use case myself to practice building interactive dashboards with Plotly https://plot.ly/python/ and Dash https://dash.plot.ly/ Python libraries. If you are interested in source code, please visit this GitHub repository.'),
        html.P('Please note that all charts are interactive - you can hoover over the charts to display more details, or use the tool bar in the charts to zoom-in / zoom-out.'),
        html.H2('Does it rain more often in winter or in summer?'),
        html.P('Autumn is usally belived to be the most rainy season of the year. However the charts below depicts, that (in the long-term average) the number of rainy days does not much vary throughout the year (10 - 14 days each month).'),
        dcc.Graph(id='scatterplot',
                figure={'data':data,
                        'layout':layout,
                        'config':pyo_config
                        })
])
# server clause
if __name__ == '__main__':
    app.run_server()
