from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask("hubei level up")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

@app.route('/')
def index():
    return None

@app.route('/table')
def table():
    return None

@socketio.on('join')
def on_join(player):
    

@socketio.on('json')
def handle_json(json):
