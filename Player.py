import random
import bisect

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
            if self.lastDrawn:
                json["lastDrawn"] = self.lastDrawn.toJSON()
            else:
                json["lastDrawn"] = None
            json["actions"] = self.actions
        return json

    def startGame(self, direction):
        self.direction = direction
        self.score = 0
        self.hand = []
        self.handSize = 0
        self.completed = []
        self.actions = []
        self.lastDrawn = None

    def changeIcon(self, index):
        self.iconIndex = index

    def changeName(self, newName):
        self.playerName = newName

    def ready(self, readyStatus):
        self.isReady = readyStatus

    def setHand(self, cards):
        self.hand = cards
        self.hand.sort()
        self.handSize = len(self.hand)

    def draw(self, card):
        bisect.insort(self.hand, card)
        self.handSize = len(self.hand)
        self.lastDrawn = card

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

