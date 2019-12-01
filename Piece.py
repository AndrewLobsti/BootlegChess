class Piece:

    def __init__(self, ID, team):
        if team == 1:
            self.ID = str(ID).upper()
        else:
            self.ID = ID
        self.neverMoved = True
        self.team = team

    def __str__(self):
        return " " + str(self.ID) + " "

    __repr__ = __str__


