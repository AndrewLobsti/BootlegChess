from Piece import Piece


class Pawn(Piece):

    def __init__(self, ID, team, startingRow, c):
        super().__init__(ID, team, 1.0)
        self.startingRow = startingRow
        self.r = startingRow
        self.c = c
        self.ds = 1  # movement direction is south if this is 1
        if startingRow == 6:
            self.ds = 0
        self.promotionRow = int(startingRow - ((((startingRow - 6) + 1) / abs((startingRow - 6) + 1)) * 6))

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesList, nr, nc):
        pwp = []  # positions with pieces
        npp = "X"  # piece in the position we want to move t, if it exists
        pp = "X"  # en passant attack target, if it exists
        for p in piecesList:
            pwp.append([p.r, p.c])
            if p.r == nr and p.c == nc:
                if p.team == self.team:
                    return False
                npp = p
            if p.r == self.r and p.c == nc and p.team != self.team:
                pp = p
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
                if npp != "X":
                    return True
                elif pp != "X":
                    if pp.type == "p":  # En passant attack code
                        if abs(self.r - pp.startingRow) == 2 and pp.moves == 1:
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
