import random
from threading import Timer

from Player import Player
from Card import Card

from constants import turnTime, actionTime, bufferTime

class Game():
    def __init__(self, roomCode):
        self.roomCode = roomCode
        self.started = False
        self.stopped = False
        self.gameOver = False
        self.players = []

        self.timer = None
    
    def getLobbyDataJSON(self, sessionID):
        json = {}
        json["roomCode"] = self.roomCode
        json["players"] = []
        for i in range(len(self.players)):
            if self.players[i].sessionID == sessionID:
                json["currentPlayer"] = self.players[i].getLobbyPlayerJSON()
            else:
                json["players"].append(self.players[i].getLobbyPlayerJSON())
        return json

    def getGameDataJSON(self, sessionID):
        json = {}
        json["roomCode"] = self.roomCode
        json["direction"] = self.direction.toJSON()
        json["turn"] = self.turn.toJSON()
        json["actionTurn"] = self.actionTurn
        json["winner"] = self.winner
        json["players"] = []
        for i in range(len(self.players)):
            if self.players[i].sessionID == sessionID:
                json["currentPlayer"] = self.players[i].getGamePlayerJSON(True)
                for j in range(1,4):
                    json["players"].append(self.players[(i + j)%4].getGamePlayerJSON(False))
        json["discardPile"] = [x.toJSON() for x in self.discardPile]
        json["drawPile"] = self.drawPile
        return json

    def changeTurn(self):
        self.turn.num += 1
        if self.turn.num == 5:
            self.turn.num = 1

    def discard(self, sessionID, index):
        for p in self.players:
            if p.sessionID == sessionID:
                discarded = p.discard(index)
                self.discardPile.insert(0, discarded)
                break
        self.actionTurn = True

    def action(self, sessionID, index):
        self.actionsReceived[sessionID] = index
        if len(self.actionsReceived) == 4:
            self.actionsReceived.clear()
            self.changeTurn()
            self.actionTurn = False
            return True
        return False

    def createCode(self, len):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(letters) for l in range(len))

    # Returns a random 8 uppercase letter sequence thats not already in use
    def addPlayer(self, isHost, sessionID):
        self.players.append(Player(isHost, sessionID))

    def removePlayer(self, sessionID):
        for i in range(len(self.players)):
            if self.players[i].sessionID == sessionID:
                popped = self.players.pop(i)
                if popped.isHost: # pass host along
                    for p in self.players:
                        p.isHost = True
                        p.isReady = True
                        break
                return not self.players
    
    def changeIcon(self, sessionID, index):
        for p in self.players:
            if p.sessionID == sessionID:
                p.changeIcon(index)

    def changeName(self, sessionID, newName):
        for p in self.players:
            if p.sessionID == sessionID:
                p.changeName(newName)

    def playerReady(self, sessionID, readyStatus):
        for p in self.players:
            if p.sessionID == sessionID:
                p.ready(readyStatus)

    def canStart(self, sessionID):
        if len(self.players) != 4:
            return False
        for p in self.players:
            if p.sessionID == sessionID: 
                if not p.isHost:
                    return False
        for p in self.players:
            if not p.isReady:
                return False
        return True

    def startGame(self):
        self.direction = Card.special(1)
        self.turn = Card.special(1)
        self.actionTurn = False
        self.winner = None
        for i in range(1, len(self.players) + 1):
            self.players[i - 1].startGame(Card.special(i))
        self.discardPile = []
        self.drawPile = 420
        self.actionsReceived = {}

    def startDiscardTimer(self, callBack):
        self.cancelTimer()
        self.timer = Timer(turnTime + bufferTime, self.defaultDiscard, [callBack])
        self.timer.start()

    def startActionTimer(self, callBack):
        self.cancelTimer()
        self.timer = Timer(actionTime + bufferTime, self.defaultAction, [callBack])
        self.timer.start()

    def defaultDiscard(self, callBack):
        self.cancelTimer()
        self.discard(self.playerFromDirection(self.turn).sessionID, 0)
        callBack(self.roomCode)
        self.startActionTimer(callBack)

    def defaultAction(self, callBack):
        self.cancelTimer()
        for p in self.players:
            if p.sessionID not in self.actionsReceived:
                shouldNotify = self.action(p.sessionID, -1)
                if shouldNotify:
                    break
        callBack(self.roomCode)
        self.startDiscardTimer(callBack)

    def cancelTimer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def playerFromDirection(self, direction):
        for p in self.players:
            if p.direction == direction:
                return p
        print(f"Player not found given direction {direction}")

    def playerFromSessionID(self, sessionID):
        for p in self.players:
            if p.sessionID == sessionID:
                return p
        print(f"Player not found given session ID {sessionID}")
