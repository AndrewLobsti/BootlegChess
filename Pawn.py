from Piece import Piece


class Pawn(Piece):

    def __init__(self, ID, team, startingRow):
        super().__init__(ID, team)
        self.startingRow = startingRow
        self.ds = 1
        if startingRow == 7:
            self.ds = 0
        self.promotionRow = int(startingRow - ((((startingRow - 7) + 1) / abs((startingRow - 7) + 1)) * 6))

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if board.validIndex(nr, nc):
            if nr == cr and nc == cc:
                return False
            maxRange = 1
            if nc != cc:
                if nr == cr:
                    return False
                if self.ds == 0:
                    if nr > cr:
                        return False
                else:
                    if nr < cr:
                        return False
                if abs(nr - cr) > maxRange or abs(nc - cc) > maxRange:
                    return False
                else:
                    if not str(board.square(nr, nc)).isspace():
                        if board.square(nr, nc).team != self.team:
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                if nr == cr:
                    return False
                if self.ds == 0:
                    if nr > cr:
                        return False
                else:
                    if nr < cr:
                        return False
                if self.neverMoved:
                    maxRange = 2
                if abs(nr - cr) > maxRange:
                    return False
                if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                    nb = 1
                    cb = 1
                else:
                    nb = 0
                    cb = 0
                for r in range(nr - int((abs(nr - cr) + (nr - cr)) / 2) + nb, cr + int((abs(nr - cr) + (nr - cr)) / 2) + cb):
                    if not str(board.square(r, cc)).isspace():
                        return False
                return True
        else:
            return False
