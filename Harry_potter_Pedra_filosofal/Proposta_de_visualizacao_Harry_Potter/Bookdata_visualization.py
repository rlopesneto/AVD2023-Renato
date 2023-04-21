import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Data from your CSV
data = '''
28323   -60.5   4829
20918   -67.0   3658
23949   -85.0   4209
21936   -78.0   3855
41738   -65.0   7107
38303   -57.5   6688
27461   -38.0   4662
19219   -47.0   3300
30873   -90.5   5366
27169   -49.5   4686
20842   -27.5   3606
33041   -55.0   5772
19718   -22.5   3412
21366   -49.0   3737
31097   -106.0  5328
38878   -91.0   6739
33245   -46.5   5766
'''

# Convert data to a pandas DataFrame
data = [row.split() for row in data.strip().split('\n')]
df = pd.DataFrame(data, columns=['Chapter', 'Sentiment', 'WordCount'])

# Convert columns to appropriate data types
df['Chapter'] = df['Chapter'].astype(int)
df['Sentiment'] = df['Sentiment'].astype(float)
df['WordCount'] = df['WordCount'].astype(int)

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Book Data Visualization", className="text-center my-4"),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Choose a visualization:"),
            dcc.Dropdown(
                id="visualization_dropdown",
                options=[
                    {"label": "Bar plot for Sentiment", "value": "bar_sentiment"},
                    {"label": "Scatter plot for Sentiment vs Word Count", "value": "scatter_sentiment_wordcount"},
                    {"label": "Line plot for Sentiment", "value": "line_sentiment"}
                ],
                value="bar_sentiment",
            ),
            dcc.Graph(id="visualization_graph")
        ])
    ])
], fluid=True)

# Callback to update the graph based on the dropdown selection
@app.callback(
    Output("visualization_graph", "figure"),
    [Input("visualization_dropdown", "value")]
)
def update_graph(visualization):
    if visualization == "bar_sentiment":
        fig = px.bar(df, x=df.index + 1, y='Sentiment', labels={'x': 'Chapter Number', 'y': 'Sentiment'})
    elif visualization == "scatter_sentiment_wordcount":
        fig = px.scatter(df, x='WordCount', y='Sentiment', color=df.index + 1, hover_data=['Chapter'], labels={'x': 'Word Count', 'y': 'Sentiment', 'color': 'Chapter Number'})
    elif visualization == "line_sentiment":
        fig = px.line(df, x=df.index + 1, y='Sentiment', labels={'x': 'Chapter Number', 'y': 'Sentiment'}, title='Sentiment by Chapter')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

