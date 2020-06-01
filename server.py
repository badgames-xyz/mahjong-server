import os
import time
import random
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import sys
from Game import Game

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

games = {}

def notifyAll(roomCode):
    for p in games[roomCode].players:
            player = games[roomCode].players[p]
            emit('lobbyData', games[roomCode].getLobbyDataJSON(player.sessionID), room=player.sessionID)

@socketio.on('join')
def onJoin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 1})
        return
    games[roomCode].addPlayer(False, request.sid)
    notifyAll(roomCode)

@socketio.on('create')
def onCreate(data):
    game = Game()
    games[game.roomCode] = game
    game.addPlayer(True, request.sid)
    emit('lobbyData', game.getLobbyDataJSON(request.sid))

@socketio.on('leave')
def onLeave(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 3})
        return
    games[roomCode].removePlayer(request.sid)
    notifyAll(roomCode)

@socketio.on('changeName')
def onNameChange(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    newName = data["name"]
    if roomCode not in games:
        emit('error', {'code': 2})
        return
    games[roomCode].changeName(request.sid, newName)
    notifyAll(roomCode)

@socketio.on('ready')
def onReady(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 4})
        return
    games[roomCode].playerReady(request.sid, True)
    notifyAll(roomCode)

@socketio.on('notReady')
def onNotReady(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 5})
        return
    games[roomCode].playerReady(request.sid, False)
    notifyAll(roomCode)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])