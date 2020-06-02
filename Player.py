import random

allTiles = {}
availableTiles = []

class Player:
    def __init__(self, playerID, isHost, sessionID):
        names = ["Md Devlin", "Huxley Atkins", "Bilaal Sheldon", "Mark Dalton", "Tahlia Dunn", "Tala Case", "Francesca Campbell", "Rex Cassidy", "Suranne Guest", "Jamal Bridges"]
        self.playerID = playerID
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

    def getPlayerJSON(self):
        json = {}
        json["id"] = self.playerID
        json["name"] = self.playerName
        json["iconIndex"] = self.iconIndex
        json["isHost"] = self.isHost
        json["ready"] = self.isReady
        return json

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