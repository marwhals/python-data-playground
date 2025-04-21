import random
import numpy as np
import threading
import time

import dash
import plotly.graph_objs as go
from dash import dcc, html
from flask import Flask
from flask_socketio import SocketIO, emit

# Create the Flask server and initialize Flask-SocketIO
server = Flask(__name__)
app = dash.Dash(__name__, server=server)
socketio = SocketIO(server)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Real-time Data Dashboard"),
    dcc.Graph(id="live-update-graph"),
    dcc.Interval(
        id="interval-component",
        interval=1 * 1000,  # Update every 1 second
        n_intervals=0
    )
])


# Callback to update the graph using WebSocket
@app.callback(
    dash.dependencies.Output("live-update-graph", "figure"),
    [dash.dependencies.Input("interval-component", "n_intervals")]
)
def update_graph(n):
    # Generate random data for x and y
    x = list(range(100))  # X values from 0 to 100
    y = [random.randint(1, 100) for _ in range(100)]  # Random Y values between 1 and 100

    figure = {
        'data': [
            go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',  # Use lines+markers to make the updates clear
            )
        ],
        'layout': go.Layout(
            title="Live Data Stream (Random)",
            xaxis={'title': 'X Value'},
            yaxis={'title': 'Y Value'},
        )
    }
    return figure


# WebSocket handler for broadcasting data
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to WebSocket server'})


# Broadcast random data to all connected clients
def broadcast_data():
    while True:
        # Generate random data for x and y
        x = list(range(100))  # X values from 0 to 100
        y = [random.randint(1, 100) for _ in range(100)]  # Random Y values between 1 and 100
        data = {
            'x': x,  # X values
            'y': y   # Random Y values
        }
        socketio.emit('update', data, broadcast=True)  # Broadcast data to all clients
        time.sleep(1)  # Send new data every 1 second


# Run the data broadcasting in a separate thread
thread = threading.Thread(target=broadcast_data)
thread.daemon = True
thread.start()

# WebSocket client-side update
@socketio.on('update')
def handle_update(data):
    print(f"Received update: {data}")
    # Update the Dash graph here
    app.layout['live-update-graph'].update(data)

# Run the app with SocketIO
if __name__ == "__main__":
    socketio.run(server, debug=True, allow_unsafe_werkzeug=True)
