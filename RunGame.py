# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 05:40:22 2019

@author: Brian Yung
"""
#Setup game players and tiles
#Functions that make the game work

from Player import *
from Tile import *
from websockets import *

#Variables
dontDraw = True
seats = ["East","South","West","North"]

#Replace with player data (id,name) from lobby
players = [Player(0,{},1500,""),
           Player(1,{},1500,""),
           Player(2,{},1500,""),
           Player(3,{},1500,"")]

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
    
    #Setting up player seating
    random.shuffle(players)
    for seatDeicide in range(0,4):
        players[seatDeicide].seat = seats[seatDeicide]
    
    #Setup starting hand for each player, East seat player gets the first turn
    for playerDrawing in players:
        if (playerDrawing.seat == "East"):
            for numToDraw in range(0,14):
                playerDrawing.draw()
        else:
            for numToDraw in range(0,13):
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

def gameRound():
    #Play through the round until tiles run out
    while availableTiles:
        for playerTurn in players:
            turn(playerTurn)
        if not availableTiles:
            break