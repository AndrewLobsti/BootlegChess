from Piece import Piece


class Bishop(Piece):

    def __init__(self, ID, team, r, c):
        super().__init__(ID, team, 3.25)
        self.r = r
        self.c = c

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesOnBoard, nr, nc):
        cc = self.c
        cr = self.r
        pwp = []
        npp = "X"
        for p in piecesOnBoard:
            if p.r == nr and p.c == nc:
                npp = p
            pwp.append([p.r, p.c])
        if nr == cr and nc == cc:
            return False
        if npp != "X":
            if npp.team == self.team:
                return False
        if abs(nr - cr) == abs(nc - cc):
            if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                nb = 1
            else:
                nb = 0
            rowScanStart = nr - int((abs(nr - cr) + (nr - cr)) / 2)
            rowScanEnd = cr + int((abs(nr - cr) + (nr - cr)) / 2) + nb
            for r in range(rowScanStart, rowScanEnd):
                c = int(cc + ((nc - cc) / abs(nc - cc)) * abs(r - cr))
                if c != cc and c != nc and r != cr and r != nr:
                    if pwp.count([r, c]) > 0:
                        return False
            return True
        else:
            return False
