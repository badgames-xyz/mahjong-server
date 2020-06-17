from Card import Card

class Action:
    def __init__(self, group, start, taken, win=False):
        self.group = group
        self.start = start
        self.taken = taken
        self.cards = self.createCards()
        self.winningAction = win

    @classmethod
    def chow(cls, start, taken):
        return Action("chow", start, taken)

    @classmethod
    def pong(cls, start, taken):
        return Action("pong", start, taken)

    @classmethod
    def kong(cls, start, taken):
        return Action("kong", start, taken)

    @classmethod
    def winChow(cls, start, taken):
        return Action("win chow", start, taken, win=True)

    @classmethod
    def winPong(cls, start, taken):
        return Action("win pong", start, taken, win=True)

    @classmethod
    def winKong(cls, start, taken):
        return Action("win kong", start, taken, win=True)

    @classmethod
    def winEyes(cls, start, taken):
        return Action("win eyes", start, taken, win=True)

    @classmethod
    def placeKong(cls, start, taken):
        return Action("place kong", start, taken)

    @classmethod
    def addKong(cls, start, taken):
        return Action("add kong", start, taken)

    def createCards(self):
        cards = []
        if "chow" in self.group:
            cards = [self.start.copy(), self.start.up(), self.start.up().up()]
        elif "pong" in self.group:
            cards = [self.start.copy(), self.start.copy(), self.start.copy()]
        elif "kong" in self.group:
            cards = [self.start.copy(), self.start.copy(), self.start.copy(), self.start.copy()]
        elif "eyes" in self.group:
            cards = [self.start.copy(), self.start.copy()]
        else:
            print("Invalid Action Created")
        return cards

    def toJSON(self):
        return {
            "type": self.group,
            "taken": self.taken.toJSON(),
            "cards": [x.toJSON() for x in self.cards],
        }

    def cardsJSON(self, isCurrentPlayer):
        if not isCurrentPlayer and self.group == "place kong":
            return [Card.hidden().toJSON() for x in self.cards]
        else:
            return [x.toJSON() for x in self.cards]
