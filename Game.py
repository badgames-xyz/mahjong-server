import random
from threading import Timer

from Player import Player
from Card import Card, createDeck

from constants import turnTime, actionTime, bufferTime, timeBetweenGames
import time

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
        if self.actionTurn:
            json["time"] = actionTime
        else:
            json["time"] = turnTime
        json["timeLeft"] = 0 # TODO
        json["newGame"] = self.newGame
        for i in range(len(self.players)):
            if self.players[i].sessionID == sessionID:
                json["currentPlayer"] = self.players[i].getGamePlayerJSON(True)
                for j in range(1,4):
                    json["players"].append(self.players[(i + j)%4].getGamePlayerJSON(False))
        json["discardPile"] = [x.toJSON() for x in self.discardPile]
        json["drawPile"] = self.drawPile
        return json

    def resetAllLastDrawn(self):
        for p in self.players:
            p.lastDrawn = None

    def removeDiscardCard(self):
        self.discardPile.pop(0)

    def changeTurn(self, sessionID):
        self.turn = self.playerFromSessionID(sessionID).direction

    def discard(self, sessionID, index):
        discarded = self.playerFromSessionID(sessionID).discard(index)
        self.discardPile.insert(0, discarded)
        for p in self.players:
            p.resetActions()
        self.createActions(sessionID, discarded)
        self.actionTurn = True
        # player discarding can only pass
        self.action(sessionID, -1)
        self.newGame = False
        self.resetAllLastDrawn()

    def createActions(self, sid, card):
        numPlayers = len(self.players)
        ind = 0
        for i in range(numPlayers):
            if self.players[i].sessionID == sid:
                ind = i
                break
        for i in range(1, numPlayers):
            p = self.players[(ind + i) % numPlayers]
            if (i == 1):
                p.createActions(card, True)
            else:
                p.createActions(card)

    def action(self, sessionID, index):
        self.actionsReceived[sessionID] = index
        if len(self.actionsReceived) == 4:
            self.clearRecentActions()
            # given all actions, determine who gets it
            numPlayers = len(self.players)
            curPlayer = self.playerFromDirection(self.turn)
            ind = 0
            for i in range(numPlayers):
                if self.players[i].sessionID == curPlayer.sessionID:
                    ind = i
                    break
            settled = False

            nextPlayer = self.players[(ind + 1) % numPlayers].sessionID
            anyoneWants = False
            for sid in self.actionsReceived:
                if self.actionsReceived[sid] >= 0:
                    anyoneWants = True
                    break

            if anyoneWants:
                # check winning moves in counter clockwise order
                for i in range(1, numPlayers):
                    p = self.players[(ind + i) % numPlayers]
                    actionIndex = self.actionsReceived[p.sessionID]
                    if actionIndex == -1:
                        continue
                    action = p.actions[actionIndex]
                    if action.winningAction:
                        # give it to this player.
                        p.doAction(action)
                        self.removeDiscardCard()
                        self.win(p.sessionID)
                        return True

                if not settled:
                    # check pong/kong in clockwise order
                    for i in range(1, numPlayers):
                        p = self.players[ind - i]
                        actionIndex = self.actionsReceived[p.sessionID]
                        if actionIndex == -1:
                            continue
                        action = p.actions[actionIndex]
                        p.doAction(action)
                        self.removeDiscardCard()
                        if action.group == "kong":
                            p.draw(self.deck.pop())
                            self.drawPile = len(self.deck)
                        p.recentAction = True
                        settled = True
                        nextPlayer = p.sessionID
                        break

                if not settled:
                    # check for chow
                    p = self.players[(ind + 1) % numPlayers]
                    actionIndex = self.actionsReceived[p.sessionID]
                    if actionIndex != -1:
                        action = p.actions[actionIndex]
                        p.doAction(action)
                        self.removeDiscardCard()
                        nextPlayer = p.sessionID
                    p.recentAction = True
            else:
                # everyone passes, next player draws a card
                self.playerFromSessionID(nextPlayer).draw(self.deck.pop())
                self.drawPile = len(self.deck)

            self.actionsReceived.clear()
            self.changeTurn(nextPlayer)
            self.actionTurn = False
            return True
        return False

    def win(self, sessionID):
        winner = self.playerFromSessionID(sessionID)
        self.winner = sessionID
        if winner.direction == Card.special(1):
            self.winStreak += 1
        else:
            self.winStreak = 0
        selfDrew = winner.recentAction
        winner.updateMoney(self.winStreak, selfDrew)

    def clearRecentActions(self):
        for p in self.players:
            p.recentAction = False

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
        self.playerFromSessionID(sessionID).changeIcon(index)

    def changeName(self, sessionID, newName):
        self.playerFromSessionID(sessionID).changeName(newName)

    def playerReady(self, sessionID, readyStatus):
        self.playerFromSessionID(sessionID).ready(readyStatus)

    def canStart(self, sessionID):
        if len(self.players) != 4:
            return False
        player = self.playerFromSessionID(sessionID)
        if not player.isHost:
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
        self.deck = createDeck()
        self.actionsReceived = {}
        self.gamesPlayed = 0
        self.winStreak = 0
        self.newGame = True

        # all players draw 13 cards, first player draws 14
        for p in self.players:
            p.setHand([self.deck.pop() for i in range(13)])
        self.players[0].draw(self.deck.pop())
        self.drawPile = len(self.deck)

    def nextGame(self):
        changeDirection = self.winStreak == 0
        self.gamesPlayed += 1
        if self.gamesPlayed % 4 == 0:
            self.direction = self.direction.nextDirection()
        self.turn = Card.special(1)
        self.actionTurn = False
        self.winner = None
        for p in self.players:
            p.nextGame(changeDirection)
        self.discardPile = []
        self.deck = createDeck()
        self.drawPile = len(self.deck)
        self.actionsReceived = {}
        self.newGame = True

        # all players draw 13 cards, first player draws 14
        for p in self.players:
            p.setHand([self.deck.pop() for i in range(13)])
        self.playerFromDirection(self.turn).draw(self.deck.pop())


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
                if shouldNotify and self.winner is not None:
                    callBack(self.roomCode)
                    # wait a few seconds then start the next game
                    time.sleep(timeBetweenGames)
                    self.nextGame()
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
