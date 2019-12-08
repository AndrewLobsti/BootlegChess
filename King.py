from Piece import Piece


class King(Piece):

    def __init__(self, ID, team, r, c):
        super().__init__(ID, team, 1000.0)
        self.r = r
        self.c = c

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesOnBoard, nr, nc):
        if nr == self.r and nc == self.c:
            return False
        if abs(nr - self.r) > 1:
            return False
        cc = self.c
        cr = self.r
        pwp = []
        npp = "X"
        for p in piecesOnBoard:
            if p.r == nr and p.c == nc:
                npp = p
            pwp.append([p.r, p.c])
        if abs(nc - cc) == 2:  # Castling Code
            if nr != cr or self.neverMoved is False or npp != "X":
                return False
            if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                rookColumn = 7
                scanStart = cc + 1
                scanEnd = 8
            else:
                rookColumn = 0
                scanStart = 2
                scanEnd = cc
            friendlyRookInCastlingPosition = False
            for p in piecesOnBoard:
                if p.r == cr and p.c == rookColumn and p.type == "r" and p.team == self.team:
                    friendlyRookInCastlingPosition = True
            if friendlyRookInCastlingPosition:
                for c in range(scanStart, scanEnd):
                    if pwp.count([cr, c]) > 0:
                        return False
                return True
        else:
            if abs(nc - cc) > 1:
                return False
            if nc != cc and nr != cr:
                if abs(nc - cc) != abs(nr - cr):
                    return False
            if npp != "X":
                if npp.team != self.team:
                    return True
                else:
                    return False
            else:
                return True
