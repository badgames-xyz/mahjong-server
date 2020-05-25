class Tile:
    def __init__(self, suit, number):
        self.suit = suit
        self.num = number
        
    def __str__(self):
        return str((self.suit,self.num))
    
    def __repr__(self):
        return str((self.suit,self.num))
    
    def __lt__(self, other):
        return self.suit < other.suit or self.num < other.num
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.suit == other.suit and self.num == other.num