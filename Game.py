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
            json["players"].append(self.players[p].getPlayerJSON())
            if self.players[p].sessionID == sessionID:
                json["currentPlayer"] = self.players[p].getPlayerJSON()
        return json

    def createCode(self, len):
        letters = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choice(letters) for l in range(len))

    # Returns a random 8 uppercase letter sequence thats not already in use
    def addPlayer(self, isHost, sessionID):
        playerID = self.createCode(8)
        while playerID in self.players:
            playerID = self.createCode(8)
        self.players[playerID] = Player(playerID, isHost, sessionID)
