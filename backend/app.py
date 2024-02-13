from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_sock import Sock
from flask_cors import CORS
import json
from levelup import *
from threading import Thread
from gevent.pywsgi import WSGIServer

app = Flask("hubei level up", 
            static_url_path='', 
            static_folder='static',
            template_folder='static')
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
        self.view = set()
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
    user = obj['username']
    if user not in users:
        users[user] = User()
    users[user].ws = ws

    if obj['verb'] == SIT:
        if obj['table'] not in tables:
            tables[obj['table']] = Table()
        if users[user].table != None:
            if users[user].seat != None:
                if tables[users[user].table].game != None:
                    announce(obj['table'], {
                        'verb': SIT,
                        'seats': tables[obj['table']].seats
                    })
                    tables[users[user].table].game.reconnect(users[user].seat)
                    return
                else:
                    tables[users[user].table].seats[users[user].seat] = None
                    announce(users[user].table {
                        'verb': SIT,
                        'seats': tables[users[user].table].seats
                    })
            tables[users[user].table].view.remove(user)
        users[user].table = obj['table']
        tables[users[user].table].view.add(user)

        if obj['seat'] in range(4) and tables[obj['table']].seats[obj['seat']] == None:
            tables[obj['table']].seats[obj['seat']] = user
            users[user].seat = obj['seat']
        else:
            users[user].seat = None
            
        announce(obj['table'], {
            'verb': SIT,
            'seats': tables[obj['table']].seats
        })

    elif obj['verb'] == READY:
        table = users[user].table
        if user not in tables[table].seats:
            return
        if tables[table].game:
            # todo: reconnect to game
            pass
        else:
            if obj['dealer'] not in [-1, 0, 1, 2, 3]:
                return
            if obj['level'] not in ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                return
            game = Game(table, [(i == None) for i in tables[table].seats], obj['dealer'], obj['level'])
            game.tell_callback = tell
            game.announce_callback = announce
            t = Thread(target=run_game, args=[game])
            t.start()
    else:
        table = users[user].table
        seat  = users[user].seat
        print(table, seat, obj)
        if table == None or seat == None or tables[table].game == None:
            return
        if obj['verb'] == COLOR:
            tables[table].game.declare(seat, obj['card'])
        elif obj['verb'] == PLAY:
            tables[table].game.player_play(seat, obj['cards'])
        elif obj['verb'] == BOTTOM:
            tables[table].game.dealer_select_bottom(seat, obj['cards'])

def tell(table, player, obj):
    user = tables[table].seats[player]
    if user == None:
        return
    ws = users[user].ws
    if ws == None:
        return
    message = json.dumps(obj)
    try:
        ws.send(message)
    except:
        print(user, "disconnected.")
        users[user].ws = None

def announce(table, obj):
    for user in tables[table].view:
        ws = users[user].ws
        if ws == None:
            return
        message = json.dumps(obj)
        try:
            ws.send(message)
        except:
            print(user, "disconnected.")
            users[user].ws = None

@app.route('/')
def page():
    return render_template('index.html')

@sockets.route('/ws')
def echo_socket(ws):
    while True:
        message = ws.receive()
        obj = json.loads(message)
        operation(ws, obj)

# app.run()
if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
