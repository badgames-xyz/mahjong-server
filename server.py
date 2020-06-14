import os
import time
import random
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import sys

from Game import Game
from constants import codes, timeBetweenGames

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

timer = None

games = {}
timers = {}

def lobbyNotifyAll(roomCode):
    for p in games[roomCode].players:
        emit('lobbyData', games[roomCode].getLobbyDataJSON(p.sessionID), room=p.sessionID)

def gameNotifyAll(roomCode):
    for p in games[roomCode].players:
        emit('gameData', games[roomCode].getGameDataJSON(p.sessionID), room=p.sessionID)

def gameTimerNotifyAll(roomCode):
    for p in games[roomCode].players:
        socketio.emit('gameData', games[roomCode].getGameDataJSON(p.sessionID), room=p.sessionID)

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
    code = createRoomCode()
    game = Game(code)
    games[code] = game
    game.addPlayer(True, request.sid)
    emit('lobbyData', game.getLobbyDataJSON(request.sid))

def createRoomCode():
    if len(games) == len(codes):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(letters) for l in range(4))
    else:
        code = random.choice(codes)
        while code in games:
            code = random.choice(codes)
        return code

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
    games[roomCode].startDiscardTimer(gameTimerNotifyAll)

@socketio.on('discard')
def onDiscard(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 10})
        return
    games[roomCode].discard(request.sid, data["index"])
    gameNotifyAll(roomCode)
    games[roomCode].startActionTimer(gameTimerNotifyAll)

@socketio.on('action')
def onAction(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 11})
        return
    shouldNotify = games[roomCode].action(request.sid, data["index"])
    if shouldNotify:
        if games[roomCode].winner is not None:
            nextGame(roomCode)
        else:
            gameNotifyAll(roomCode)
            games[roomCode].startDiscardTimer(gameTimerNotifyAll)

@socketio.on('win')
def onWin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    # check if can win first
    game = games[roomCode]
    if game.canWin():
        game.win(request.sid)
        nextGame(roomCode)

def nextGame(roomCode):
    gameNotifyAll(roomCode)
    # wait a few seconds then start the next game
    time.sleep(timeBetweenGames)
    games[roomCode].nextGame()
    gameNotifyAll(roomCode)
    games[roomCode].startDiscardTimer(gameTimerNotifyAll)
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])