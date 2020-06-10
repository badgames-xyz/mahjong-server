import os
import time
import random
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import sys
from threading import Timer
from Game import Game
from roomcodes import codes

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

turnTime = 30
actionTime = 10
bufferTime = 3

timer = None

games = {}

def lobbyNotifyAll(roomCode):
    for p in games[roomCode].players:
            emit('lobbyData', games[roomCode].getLobbyDataJSON(p.sessionID), room=p.sessionID)

def gameNotifyAll(roomCode):
    for p in games[roomCode].players:
            #emit('gameData', dummy, room=player.sessionID)
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
    timer = Timer(turnTime + bufferTime, defaultDiscard, [roomCode, request.sid])
    timer.start()

@socketio.on('discard')
def onDiscard(data):
    global timer
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 10})
        return
    if timer is not None:
        timer.cancel()
        timer = None
    games[roomCode].discard(request.sid, data["index"])
    gameNotifyAll(roomCode)
    timer = Timer(actionTime + bufferTime, defaultAction, [roomCode])
    timer.start()

@socketio.on('action')
def onAction(data):
    global timer
    data = json.loads(data)
    roomCode = data["roomCode"]
    if roomCode not in games:
        emit('error', {'code': 11})
        return
    shouldNotify = games[roomCode].action(request.sid, data["index"])
    if shouldNotify:
        if timer is not None:
            timer.cancel()
            timer = None
        gameNotifyAll(roomCode)
        nextPlayerSID = ""
        for p in games[roomCode].players:
            if games[roomCode].turn["num"] == p.direction["num"]:
                nextPlayerSID = p.sessionID
                break
        if (nextPlayerSID == ""):
            emit('error', {'code': 12})
            return
        timer = Timer(turnTime + bufferTime, defaultDiscard, [roomCode, nextPlayerSID])
        timer.start()


@socketio.on('win')
def onWin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]

def defaultDiscard(roomCode, sessionID):
    games[roomCode].discard(sessionID, 0)
    gameTimerNotifyAll(roomCode)
    timer = Timer(actionTime + bufferTime, defaultAction, [roomCode])
    timer.start()

def defaultAction(roomCode):
    for p in games[roomCode].players:
        if p.sessionID not in games[roomCode].actionsReceived:
            shouldNotify = games[roomCode].action(p.sessionID, -1)
            if shouldNotify:
                break
    gameTimerNotifyAll(roomCode)
    nextPlayerSID = ""
    for p in games[roomCode].players:
        if games[roomCode].turn["num"] == p.direction["num"]:
            nextPlayerSID = p.sessionID
            break
    if (nextPlayerSID == ""):
        emit('error', {'code': 13})
        return
    timer = Timer(turnTime + bufferTime, defaultDiscard, [roomCode, nextPlayerSID])
    timer.start()
    


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])