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

    def createCards(self):
        cards = []
        if self.group == "chow" or self.group == "win chow":
            cards = [self.start.copy(), self.start.up(), self.start.up().up()]
        elif self.group == "pong" or self.group == "win pong":
            cards = [self.start.copy(), self.start.copy(), self.start.copy()]
        elif self.group == "kong" or self.group == "win kong":
            cards = [self.start.copy(), self.start.copy(), self.start.copy(), self.start.copy()]
        elif self.group == "eyes" or self.group == "win eyes":
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
