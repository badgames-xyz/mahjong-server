import random

allTiles = {}
availableTiles = []

class Player:
    def __init__(self,userNum,hand,coins,seat,host):
        self.user = userNum
        self.hand = hand
        self.coins = coins
        self.seat = seat
        self.host = host
    
    def __repr__(self):
        return str((self.user,self.hand,self.coins,self.seat))
    
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