from Card import Card

class Action:
    def __init__(self, group, start, taken):
        self.group = group
        self.start = start
        self.taken = taken
        self.cards = self.createCards()

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
    def eyes(cls, start, taken):
        return Action("eyes", start, taken)

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
            "taken": self.taken.toJSON(),
            "cards": [x.toJSON() for x in self.cards],
        }
