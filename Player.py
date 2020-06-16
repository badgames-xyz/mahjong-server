import random
import bisect

from constants import names, numIcons
from Card import Card, suits
from Action import Action

allTiles = {}
availableTiles = []

class Player:
    def __init__(self, isHost, sessionID):
        self.sessionID = sessionID
        self.playerName = random.choice(names)
        self.iconIndex = random.randint(0, numIcons - 1)
        self.isHost = isHost
        self.isReady = isHost
        self.money = 0

    def __repr__(self):
        return str((self.user,self.hand,self.coins,self.seat))

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
        json["money"] = self.money
        json["handSize"] = self.handSize
        json["completed"] = [[c.toJSON() for c in x] for x in self.completed]
        if isCurrentPlayer:
            json["hand"] = [x.toJSON() for x in self.hand]
            if self.lastDrawn:
                json["lastDrawn"] = self.lastDrawn.toJSON()
            else:
                json["lastDrawn"] = None
            json["actions"] = [x.toJSON() for x in self.actions]
            json["canWin"] = self.canWin()
        return json

    def startGame(self, direction):
        self.direction = direction
        self.money = 0
        self.hand = []
        self.handSize = 0
        self.completed = []
        self.actions = []
        self.lastDrawn = None
        self.recentAction = False

    def nextGame(self, changeDirection=True):
        self.hand = []
        self.handSize = 0
        self.completed = []
        self.actions = []
        self.lastDrawn = None
        self.recentAction = False
        if changeDirection:
            self.direction = self.direction.prevDirection()

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

    def addCompleted(self, cards, extra):
        self.completed.append(cards)
        copy = [c.copy() for c in cards]
        copy.remove(extra)
        for c in copy:
            self.hand.remove(c)
        self.handSize = len(self.hand)

    def discard(self, index):
        discarded = self.hand.pop(index)
        self.handSize = len(self.hand)
        return discarded

    def createActions(self, card, nextTurn=False):
        # populate self.actions with chow, pong, kong, eyes
        # eyes only if winning, chow if nextTurn is True or if winning
        canWin = self.canWinWith(card)

        if self.hand.count(card) >= 2:
            self.actions.append(Action.pong(card, card))
            if canWin:
                self.actions.append(Action.winPong(card, card))
        if self.hand.count(card) >= 3:
            self.actions.append(Action.kong(card, card))
            if canWin:
                self.actions.append(Action.winKong(card, card))
        
        if nextTurn:
            possibleChows = card.getPossibleChows()
            for chow in possibleChows:
                canAdd = True
                for c in chow:
                    if c != card and c not in self.hand:
                        canAdd = False
                        break
                if canAdd:
                    self.actions.append(Action.chow(chow[0], card))
                    if canWin:
                        self.actions.append(Action.winChow(chow[0], card))

        if self.needEyes(card):
            self.actions.append(Action.winEyes(card, card))

    def doAction(self, action):
        self.addCompleted(action.cards, action.taken)

    def resetActions(self):
        self.actions.clear()

    def needEyes(self, card):
        # given a card, can the player use it to form the eyes to win
        if card not in self.hand:
            return False
        handCopy = [c.copy() for c in self.hand]
        handCopy.remove(card)
        for suit in suits:
            subHand = [c for c in handCopy if c.suit == suit]
            if not self.checkSubHand(subHand):
                return False
        return True

    def canWinWith(self, card):
        # given card, can the player win
        newHand = [c.copy() for c in self.hand]
        bisect.insort(newHand, card)
        return self.canWin(newHand)

    def canWin(self, givenHand=None):
        # with the given hand, can the player win
        hand = self.hand
        if givenHand:
            hand = givenHand
        
        # find x groups of 3, and one pair of eyes
        # remove a pair of eyes, then each suit is either empty or y groups of 3
        eyesChecked = []

        def copyHand(arr):
            return [c.copy() for c in arr]

        # given arr, finds eyes. If found, removes eyes from arr and returns true
        def findEyes(arr):
            for c in arr:
                if arr.count(c) >= 2 and c not in eyesChecked:
                    eyesChecked.append(c.copy())
                    arr.remove(c)
                    arr.remove(c)
                    return True
            return False

        temp = copyHand(hand)
        while findEyes(temp):
            # check each suit. Must be composed of only triples
            winning = True
            for suit in suits:
                subHand = [c.copy() for c in temp if c.suit == suit]
                if not self.checkSubHand(subHand):
                    winning = False
                    break
            if winning:
                return True
            temp = copyHand(hand)
        return False

    # given an array of cards of all the same suit, returns true if it
    # contains a valid set of triples
    def checkSubHand(self, subHand):
        if len(subHand) == 0:
            return True
        if len(subHand) % 3 != 0:
            return False
        if subHand[0].suit == "special":
            for s in subHand:
                if subHand.count(s) != 3:
                    return False
        else:
            # create an array of size 9 with values 0
            # for each card in the suit, increment its pos by 1
            # remove 3 of a kinds, then go through it with a sliding window
            count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for s in subHand:
                count[s.num - 1] += 1
            for i in range(len(count)):
                while count[i] >= 3:
                    count[i] -= 3
            for i in range(7): # sliding window of size 3
                if count[i] > 0:
                    count[i] -= 1
                    count[i + 1] -= 1
                    count[i + 2] -= 1
            for c in count:
                if c != 0:
                    return False
        return True

    def updateMoney(self, winStreak, selfDrew):
        self.money += 1
