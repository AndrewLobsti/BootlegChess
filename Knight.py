from Piece import Piece


class Knight(Piece):

    def __init__(self, ID, team, r, c):
        super().__init__(ID, team, 3.0)
        self.r = r
        self.c = c

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesOnBoard, nr, nc):
        cc = self.c
        cr = self.r
        npp = "X"
        for p in piecesOnBoard:
            if p.r == nr and p.c == nc:
                npp = p
        if nr == cr and nc == cc:
            return False
        if cc == nc or cr == nr:
            return False
        if abs(nr - cr) + abs(nc - cc) != 3:
            return False
        else:
            if npp == "X":
                return True
            else:
                if npp.team != self.team:
                    return True
                else:
                    return False
