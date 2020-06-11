import random

from constants import names, numIcons
from Card import Card

allTiles = {}
availableTiles = []

class Player:
    def __init__(self, isHost, sessionID):
        self.sessionID = sessionID
        self.playerName = random.choice(names)
        self.iconIndex = random.randint(0, numIcons - 1)
        self.isHost = isHost
        self.isReady = isHost
        self.score = 0

    def __repr__(self):
        return str((self.user,self.hand,self.coins,self.seat))
    
    #def start(self):
    #    self.user = userNum
    #    self.hand = hand
    #    self.coins = coins
    #    self.seat = seat
    #    self.host = host

    def getLobbyPlayerJSON(self):
        json = {}
        json["name"] = self.playerName
        json["iconIndex"] = self.iconIndex
        json["isHost"] = self.isHost
        json["ready"] = self.isReady
        return json
    
    def getGamePlayerJSON(self, isCurrentPlayer):
        json = {}
        json["name"] = self.playerName
        json["iconIndex"] = self.iconIndex
        json["direction"] = self.direction.toJSON()
        json["score"] = self.score
        json["handSize"] = self.handSize
        json["completed"] = self.completed
        if isCurrentPlayer:
            json["hand"] = [x.toJSON() for x in self.hand]
            json["actions"] = self.actions
        return json

    def startGame(self, direction):
        self.direction = direction
        self.score = 0
        self.hand = [
            Card.char(3),
            Card.char(6),
            Card.char(7),
            Card.char(9),
            Card.circle(1),
            Card.circle(3),
            Card.circle(4),
            Card.circle(4),
            Card.stick(2),
            Card.stick(8),
            Card.stick(8),
            Card.special(3),
            Card.special(5),
        ]
        self.handSize = len(self.hand)
        self.completed = []
        self.actions = []

    def changeIcon(self, index):
        self.iconIndex = index

    def changeName(self, newName):
        self.playerName = newName
    
    def ready(self, readyStatus):
        self.isReady = readyStatus

    def draw(self):
        tileID = random.randint(0,len(availableTiles)-1)
        drawnTile = availableTiles[tileID]
        self.hand.setdefault(drawnTile,0)
        self.hand[drawnTile] += 1
        
        allTiles[drawnTile] -= 1
        if(allTiles[drawnTile] == 0):
            availableTiles.remove(drawnTile)
    
    def discard(self, index):
        discarded = self.hand.pop(index)
        self.handSize = len(self.hand)
        return discarded
    
    def chow(self):
        "to be completed"
    
    def pong(self):
        "to be completed"
    
    def kong(self):
        "to be completed"