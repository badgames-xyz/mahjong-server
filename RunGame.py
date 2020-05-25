# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 05:40:22 2019

@author: Brian Yung
"""
#Setup game players and tiles
#Functions that make the game work

from Player import *
from Tile import *

#Variables
dontDraw = True
seats = ["East","South","West","North"]
roundCounter = 0

#Replace with player data (id,name) from lobby
playerList = [Player(0,{},1500,"East",True),
           Player(1,{},1500,"South",False),
           Player(2,{},1500,"West",False),
           Player(3,{},1500,"North",False)]

#Sets up round for game, set tiles in deck, draw tiles for players
def setupGame():
    #Setting up tiles in deck
    typesOfTile = ("Special", "Stick", "Circle", "Char")
    for types in typesOfTile:
        if (types == "Special"):
            for specialNum in range(1,8): # from 1 to 7: "East","South","West","North","Zhong","Fa cai","Bai ban"
                allTiles[Tile(types,specialNum)] = 4
        else:
            for num in range(1,10):
                allTiles[Tile(types,num)] = 4
                
    for initialTile in list(allTiles.keys()):
        availableTiles.append(initialTile)
    
    #Setup starting hand for each player, East seat player gets the first turn
    for drawing in range(0,3):
        for playerDrawing in playerList:
            for numtoDraw in range(0,4):
                playerDrawing.draw()
    for playerDrawing in playerList:
            if (playerDrawing.seat == "East"):
                for numToDraw in range(0,2):
                    playerDrawing.draw()
            else:
                playerDrawing.draw()
    
def turn(player):
    global dontDraw
    #Prompt for user ("It is player " + str(player.user) + "'s turn!\n")
    if (dontDraw == False):
        player.draw()
    
    currentHand = list(player.hand.items()) 
    currentHand = sorted(currentHand, key = lambda x: (x[0].suit, x[0].num))
    #print(currentHand) #Need to send to client
    
    position = int(input("Select a tile to discard based on position: ")) #Client input to server
    while (position > len(currentHand)):
        position = int(input("You do not have a tile in that position! Choose again")) #Server prompt to client
    selectedTile = currentHand[position][0] 
    player.discard(selectedTile)
    print("\nPlayer " + str(player.user) + " has discarded " + str(selectedTile) + "\n") #Server prompt to client
    
    dontDraw = False
    
    return selectedTile

#If someone wins, rotate player list and seat order
def rotateTurnOrder(playerList):
    global roundCounter
    playerList = playerList[1:] + playerList[:1]
    for seatChange in range(0,4):
        playerList[seatChange] = seats[seatChange]
    roundCounter += 1

def gameRound():
    #Play through the round until tiles run out
    while availableTiles:
        for playerTurn in playerList:
            turn(playerTurn)
        if not availableTiles:
            break