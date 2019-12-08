from Piece import Piece


class Pawn(Piece):

    def __init__(self, ID, team, startingRow, c):
        super().__init__(ID, team, 1.0)
        self.startingRow = startingRow
        self.r = startingRow
        self.c = c
        self.ds = 1
        if startingRow == 6:
            self.ds = 0
        self.promotionRow = int(startingRow - ((((startingRow - 6) + 1) / abs((startingRow - 6) + 1)) * 6))

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesList, nr, nc):
        pwp = []  # positions with pieces
        nppData = []
        npp = None  # piece in the position we want to move to
        for p in piecesList:
            pwp.append([p.r, p.c])
            if p.r == nr and p.c == nc:
                npp = p  # piece in the position we want to move to, if it exists
                nppData.append([p.team, p.r, p.c])
        if nr == self.r and nc == self.c:
            return False
        maxRange = 1
        if nc != self.c:
            if nr == self.r:
                return False
            if self.ds == 0:
                if nr > self.r:
                    return False
            else:
                if nr < self.r:
                    return False
            if abs(nr - self.r) > maxRange or abs(nc - self.c) > maxRange:
                return False
            else:
                if nppData.count([self.team + 1 - 2 * self.team, nr, nc]) > 0:
                    return True
                elif nppData.count([self.team + 1 - 2 * self.team, nr, nc]) > 0 and npp.type == "p":  # En passant attack code
                    if abs(self.r - npp.startingRow) == 2 and npp.moves == 1:
                        return True
            return False
        else:
            if nr == self.r:
                return False
            if self.ds == 0:
                if nr > self.r:
                    return False
            else:
                if nr < self.r:
                    return False
            if self.neverMoved:
                maxRange = 2
            if abs(nr - self.r) > maxRange:
                return False
            if int((abs(nr - self.r) + (nr - self.r)) / 2) != 0:
                nb = 1
                cb = 1
            else:
                nb = 0
                cb = 0
            for r in range(nr - int((abs(nr - self.r) + (nr - self.r)) / 2) + nb, self.r + int((abs(nr - self.r) + (nr - self.r)) / 2) + cb):
                if pwp.count([r, nc]) > 0:
                    return False
            return True
