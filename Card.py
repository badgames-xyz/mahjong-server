import random

order = {
    "char": 1,
    "circle": 2,
    "stick": 3,
    "special": 4,
}

def createDeck():
    deck = []
    for suit in order:
        lim = 10
        if suit == "special":
            lim = 8
        for num in range(1, lim):
            for i in range(4):
                deck.append(Card(suit, num))
    assert len(deck) == 136
    random.shuffle(deck)
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