from Card import Card

class Action:
    def __init__(self, group, start):
        self.group = group
        self.start = start
        self.cards = self.createCards()

    @classmethod
    def chow(cls, start):
        return Action("chow", start)

    @classmethod
    def pong(cls, start):
        return Action("pong", start)

    @classmethod
    def kong(cls, start):
        return Action("kong", start)

    @classmethod
    def eyes(cls, start):
        return Action("eyes", start)

    def createCards(self):
        cards = []
        if self.group == "chow":
            cards = [self.start.copy(), self.start.up(), self.start.up().up()]
        elif self.group == "pong":
            cards = [self.start.copy(), self.start.copy(), self.start.copy()]
        elif self.group == "kong":
            cards = [self.start.copy(), self.start.copy(), self.start.copy(), self.start.copy()]
        elif self.group == "eyes":
            cards = [self.start.copy(), self.start.copy()]
        else:
            print("Invalid Action Created")
        return cards

    def toJSON(self):
        return {
            "type": self.group,
            "cards": [x.toJSON() for x in self.cards]
        }
