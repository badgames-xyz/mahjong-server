from Player import Player
import random

class Game():
    def __init__(self):
        self.roomCode = self.createCode(4)
        self.started = False
        self.stopped = False
        self.gameOver = False
        self.players = []
    
    def getLobbyDataJSON(self, sessionID):
        json = {}
        json["roomCode"] = self.roomCode
        json["players"] = []
        for i in range(len(self.players)):
            json["players"].append(self.players[i].getLobbyPlayerJSON())
            if self.players[i].sessionID == sessionID:
                json["currentPlayer"] = self.players[i].getLobbyPlayerJSON()
        return json

    def getGameDataJSON(self, sessionID):
        json = {}
        json["direction"] = self.direction
        json["turn"] = self.turn
        json["actionTurn"] = self.actionTurn
        json["winner"] = self.winner
        json["players"] = []
        for i in range(len(self.players)):
            if self.players[i].sessionID == sessionID:
                json["currentPlayer"] = self.players[i].getGamePlayerJSON(True)
                for j in range(1,4):
                    json["players"].append(self.players[(i + j)%4].getGamePlayerJSON(False))
        json["discardPile"] = self.discardPile
        json["drawPile"] = self.drawPile
        return json


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
        self.direction = { "suit": "special", "num": 1 }
        self.turn = { "suit": "special", "num": 1 }
        self.actionTurn = False
        self.winner = None
        for i in range(1, len(self.players) + 1):
            self.players[i].startGame({ "suit": "special", "num": i })
        self.discardPile = []
        self.drawPile = 420



