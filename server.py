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

dummy = {
    'currentDirection': "north",
    'turn': "ABCD",
    'eatTurn': "",
    'winner': "",
    'players': [
        {
            'id': "ABCD",
            'name': "BOG",
            'iconIndex': "1",
            'direction': "north",
            'score': 420,
            'handSize': 13,
            'completed': [[{'suit': "circle", 'num': 6}, {'suit': "circle", 'num': 4}, {'suit': "circle", 'num': 2}]]
        },
        {
            'id': "ABCE",
            'name': "BOG2",
            'iconIndex': "1",
            'direction': "east",
            'score': 420,
            'handSize': 13,
            'completed': []
        },
        {
            'id': "ABCF",
            'name': "BOG3",
            'iconIndex': "1",
            'direction': "south",
            'score': 420,
            'handSize': 13,
            'completed': []
        },
    ],
    'currentPlayer': {
            'id': "ABCG",
            'name': "BOG4",
            'iconIndex': "1",
            'direction': "west",
            'score': 420,
            'handSize': 13,
            'completed': [[{'suit': "circle", 'num': 5}, {'suit': "circle", 'num': 6}, {'suit': "circle", 'num': 7}]],
            'eatOptions': [[{'suit': "circle", 'num': 5}, {'suit': "circle", 'num': 6}, {'suit': "circle", 'num': 7}]],
    },
    'discardPile': [{'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 4}, {'suit': "circle", 'num': 3}],
    'drawPile': 10
}



def lobbyNotifyAll(roomCode):
    for p in games[roomCode].players:
            player = games[roomCode].players[p]
            emit('lobbyData', games[roomCode].getLobbyDataJSON(player.sessionID), room=player.sessionID)

def gameNotifyAll(roomCode):
    for p in games[roomCode].players:
            player = games[roomCode].players[p]
            #emit('gameData', dummy, room=player.sessionID)
            emit('gameData', games[roomCode].getGameDataJSON(player.sessionID), room=player.sessionID)

@socketio.on('join')
def onJoin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 1})
        return
    games[roomCode].addPlayer(False, request.sid)
    lobbyNotifyAll(roomCode)

@socketio.on('refresh')
def onRefresh(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 7})
        return
    inGame = False
    for p in games[roomCode].players:
        if p.sessionID == request.sid:
            inGame = True
            break
    if not inGame:
        games[roomCode].addPlayer(False, request.sid)
    lobbyNotifyAll(roomCode)

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
    closeRoom = games[roomCode].removePlayer(request.sid)
    if closeRoom: # no more players
        games.pop(roomCode)
        return
    lobbyNotifyAll(roomCode)

@socketio.on('changeIcon')
def onIconChange(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    iconIndex = data["iconIndex"]
    if roomCode not in games:
        emit('error', {'code': 6})
        return
    games[roomCode].changeIcon(request.sid, iconIndex)
    lobbyNotifyAll(roomCode)

@socketio.on('changeName')
def onNameChange(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    newName = data["name"]
    if roomCode not in games:
        emit('error', {'code': 2})
        return
    games[roomCode].changeName(request.sid, newName)
    lobbyNotifyAll(roomCode)

@socketio.on('ready')
def onReady(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 4})
        return
    games[roomCode].playerReady(request.sid, True)
    lobbyNotifyAll(roomCode)

@socketio.on('notReady')
def onNotReady(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 5})
        return
    games[roomCode].playerReady(request.sid, False)
    lobbyNotifyAll(roomCode)

@socketio.on('startGame')
def onGameStart(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 8})
        return
    if not games[roomCode].canStart(request.sid):
        emit('error', {'code': 9})
        return
    games[roomCode].startGame()
    gameNotifyAll(roomCode)

@socketio.on('discard')
def onDiscard(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 10})
        return
    games[roomCode].discard(request.sid)

@socketio.on('action')
def onAction(data):
    data = json.loads(data)
    roomCode = data["roomCode"]

@socketio.on('win')
def onWin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])