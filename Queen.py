from Piece import Piece


class Queen(Piece):

    def __init__(self, ID, team, r, c):
        super().__init__(ID, team, 9.0)
        self.r = r
        self.c = c

    # noinspection PyAttributeOutsideInit
    def validMove(self, piecesOnBoard, nr, nc):
        # when moving diagonally will use bishop movement code, otherwise will use rook movement code
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
            if nr != cr and nc == cc:
                if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                    nb = 1
                    cb = 1
                else:
                    nb = 0
                    cb = 0
                for r in range(nr - int((abs(nr - cr) + (nr - cr)) / 2) + nb,
                               cr + int((abs(nr - cr) + (nr - cr)) / 2) + cb):
                    # this will cycle over the rows that are between where the piece is and where we want it to be.
                    # the math inside the range function will compute the number of lines (nr - cr) we add (cr +) or
                    # subtract (nr -) to go from our current row (cr) to the row we want to move to (nr, next row),
                    # or vice-versa, and will then add the distance (abs(nr - cr)) from cr to nr. It will then divide
                    # the computed value by 2. By doing this, our for function will always cycle from the smallest to
                    # biggest row, no matter the direction we want to move in, since if the first argument in the
                    # range function is to be nr then it means nr < cr, and our computation will do either nr - 0/2
                    # or cr + 0/2, and vice-versa if the first argument is to be cr. This is to be used for vertical
                    # movement.
                    if pwp.count([r, cc]) > 0:
                        if r != nr:
                            return False
                        else:
                            if npp.team == self.team:
                                return False
                return True
            elif nc != cc and nr == cr:
                if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                    nb = 1
                    cb = 1
                else:
                    nb = 0
                    cb = 0
                for c in range(nc - int((abs(nc - cc) + (nc - cc)) / 2) + nb,
                               cc + int((abs(nc - cc) + (nc - cc)) / 2) + cb):
                    # same as explained in the comment bloc above, but for lengthwise movement.
                    if pwp.count([cr, c]) > 0:
                        if c != nc:
                            return False
                        else:
                            if npp.team == self.team:
                                return False
                return True
            else:
                return False
