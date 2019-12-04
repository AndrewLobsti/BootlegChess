class Piece:

    def __init__(self, ID, team, value):
        if team == 1:
            self.ID = str(ID).upper()
        else:
            self.ID = ID
        self.neverMoved = True
        self.team = team
        self.type = str(ID)
        self.moves = 0
        self.value = value

    def __str__(self):
        return " " + str(self.ID) + " "

    __repr__ = __str__


