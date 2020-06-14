import random

order = {
    "char": 1,
    "circle": 2,
    "stick": 3,
    "special": 4,
}

suits = ["char", "circle", "stick", "special"]

def createDeck():
    deck = []
    # for suit in order:
    #     lim = 10
    #     if suit == "special":
    #         lim = 8
    #     for num in range(1, lim):
    #         for i in range(4):
    #             deck.append(Card(suit, num))
    # assert len(deck) == 136
    # random.shuffle(deck)
    for i in range(200):
        deck.append(Card.char(1))
    return deck

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num

    @classmethod
    def char(cls, num):
        return cls("char", num)

    @classmethod
    def circle(cls, num):
        return cls("circle", num)

    @classmethod
    def stick(cls, num):
        return cls("stick", num)

    @classmethod
    def special(cls, num):
        return cls("special", num)

    def toJSON(self):
        return {
            "suit": self.suit,
            "num": self.num,
        }

    def copy(self):
        return Card(self.suit, self.num)

    def up(self):
        if self.suit == "special":
            print("No up card for a special tile")
        elif self.num == 9:
            print("No up card for a 9 tile")
        else:
            return Card(self.suit, self.num + 1)

    def down(self):
        if self.suit == "special":
            print("No down card for a special tile")
        elif self.num == 1:
            print("No down card for a 1 tile")
        else:
            return Card(self.suit, self.num - 1)

    def nextDirection(self):
        if self.suit != "special" or self.num > 4:
            print("Next direction only for special direction tiles.")
        else:
            val = self.num + 1
            if val > 4:
                val = 1
            return Card.special(val)

    def getPossibleChows(self):
        chows = []
        if self.suit == "special":
            return chows
        
        if self.num >= 3:
            chows.append([self.down().down(), self.down(), self.copy()])
        if self.num >= 2 and self.num <= 8:
            chows.append([self.down(), self.copy(), self.up()])
        if self.num <= 7:
            chows.append([self.copy(), self.up(), self.up().up()])
        return chows

    def __str__(self):
        return f"Suit: {self.suit}, Num: {self.num}"
    
    def __lt__(self, other):
        if order[self.suit] < order[other.suit]:
            return True
        if order[self.suit] > order[other.suit]:
            return False
        return self.num < other.num

    def __eq__(self, other):
        return self.suit == other.suit and self.num == other.num

    def __ne__(self, other):
        return not self.__eq__(other)