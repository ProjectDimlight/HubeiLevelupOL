from flask import Flask, render_template
from flask_sock import Sock
from flask_cors import CORS
import json
from levelup import Game
from threading import Thread

app = Flask("hubei level up")
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})
sockets = Sock(app)

SIT = 100
READY = 101

tables = {
}

users = {
}

class Table:
    def __init__(self):
        self.seats = [None, None, None, None]
        self.game = None

class User:
    def __init__(self):
        self.ws = None
        self.table = None
        self.seat = None

def run_game(game):
    tables[game.table].game = game
    game.game_play()
    tables[game.table].game = None

def operation(ws, obj):
    print(obj)
    user = obj['username']
    if user not in users:
        users[user] = User()
    if users[user].ws == None:
        users[user].ws = ws
    elif users[user].ws != ws:
        return

    if obj['verb'] == SIT:
        if obj['table'] not in tables:
            tables[obj['table']] = Table()
        tables[obj['table']].seats[obj['seat']] = {
            'user': user,
            'ready': False
        }
        users[user].table = obj['table']
        users[user].seat = obj['seat']
    elif obj['verb'] == READY:
        table = users[user].table
        tables[table].seats[users[user].seat]['ready'] = True
        if tables[table].game != None:
            return
        game = Game(table, 0, '3')
        game.tell_callback = tell
        game.announce_callback = announce
        t = Thread(target=run_game, args=[game])
        t.run()

def tell(table, player, obj):
    seat = tables[table].seats[player]
    if seat == None:
        return
    ws = users[seat['user']].ws
    message = json.dumps(obj)
    ws.send(message)

def announce(table, obj):
    for seat in tables[table].seats:
        if seat == None:
            continue
        ws = users[seat['user']].ws
        message = json.dumps(obj)
        ws.send(message)

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        obj = json.loads(message)
        operation(ws, obj)

app.run()
