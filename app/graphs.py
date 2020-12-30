import plotly
import plotly.graph_objs as go
import plotly.express as px
import json

def activityDate_Graph(df):
    fig_batch = {
                    'data': [
                        go.Scatter(
                            x=df.index,
                            y=df['Number of Messages'].values,
                            # text=y,
                            # textposition='auto',
                            mode='lines'
                        )],

                    'layout': go.Layout(
                        xaxis={'title': 'Dates'},
                        yaxis={'title': 'Number of Messages'},
                        hovermode='closest',
                        title='Overall Activity of The Group'
                    )}