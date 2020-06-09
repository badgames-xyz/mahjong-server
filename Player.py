import random

allTiles = {}
availableTiles = []

class Player:
    def __init__(self, isHost, sessionID):
        names = ["Md Devlin", "Huxley Atkins", "Bilaal Sheldon", "Mark Dalton", "Tahlia Dunn", "Tala Case", "Francesca Campbell", "Rex Cassidy", "Suranne Guest", "Jamal Bridges"]
        self.playerName = random.choice(names)
        self.iconIndex = random.randint(0,3)
        self.isHost = isHost
        self.isReady = isHost
        self.sessionID = sessionID


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
        json["direction"] = self.direction
        json["score"] = self.score
        json["handSize"] = self.handSize
        json["completed"] = self.completed
        if isCurrentPlayer:
            json["hand"] = self.hand
            json["actions"] = self.actions

    def startGame(self, direction):
        self.direction = direction
        self.score = 0
        self.hand = [{'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 4}, {'suit': "circle", 'num': 3}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}, {'suit': "circle", 'num': 7}]
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
    
    def discard(self, discardTile):
        #IN PROGRESS - need to create discard pile
        self.hand[discardTile] -= 1
        if (self.hand[discardTile] == 0):
            del self.hand[discardTile]
    
    def chow(self):
        "to be completed"
    
    def pong(self):
        "to be completed"
    
    def kong(self):
        "to be completed"