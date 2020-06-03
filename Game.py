from Player import Player
import random

class Game():
    def __init__(self):
        self.roomCode = self.createCode(4)
        self.started = False
        self.stopped = False
        self.gameOver = False
        self.players = {} #dict indexed by playerID
    
    def getLobbyDataJSON(self, sessionID):
        json = {}
        json["roomCode"] = self.roomCode
        json["players"] = []
        for p in self.players:
            json["players"].append(self.players[p].getLobbyPlayerJSON())
            if self.players[p].sessionID == sessionID:
                json["currentPlayer"] = self.players[p].getLobbyPlayerJSON()
        return json

    #def getGameDataJSON(self, sessionID):


    def createCode(self, len):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(letters) for l in range(len))

    # Returns a random 8 uppercase letter sequence thats not already in use
    def addPlayer(self, isHost, sessionID):
        playerID = self.createCode(8)
        while playerID in self.players:
            playerID = self.createCode(8)
        self.players[playerID] = Player(playerID, isHost, sessionID)

    def removePlayer(self, sessionID):
        for p in self.players:
            player = self.players[p]
            if player.sessionID == sessionID:
                popped = self.players.pop(p)
                if popped.isHost: # pass host along
                    for p in self.players:
                        self.players[p].isHost = True
                        self.players[p].isReady = True
                        break
                return not self.players
    
    def changeIcon(self, sessionID, index):
        for p in self.players:
            player = self.players[p]
            if player.sessionID == sessionID:
                player.changeIcon(index)

    def changeName(self, sessionID, newName):
        for p in self.players:
            player = self.players[p]
            if player.sessionID == sessionID:
                player.changeName(newName)

    def playerReady(self, sessionID, readyStatus):
        for p in self.players:
            player = self.players[p]
            if player.sessionID == sessionID:
                player.ready(readyStatus)

    def canStart(self, sessionID):
        for p in self.players:
            player = self.players[p]
            if player.sessionID == sessionID: 
                if not player.isHost:
                    return False
        for p in self.players:
            if not player.isReady:
                return False
        return True

    #def startGame(self):
