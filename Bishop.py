from Piece import Piece


class Bishop(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team, 3)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if board.validIndex(nr, nc):
            if not str(board.square(nr, nc)).isspace():
                if board.square(nr, nc).team == self.team:
                    return False
            if abs(nr - cr) == abs(nc - cc):
                if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                    nb = 1
                else:
                    nb = 0
                if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                    cb = 1
                else:
                    cb = 0
                rowScanStart = nr - int((abs(nr - cr) + (nr - cr)) / 2) + nb
                rowScanEnd = cr + int((abs(nr - cr) + (nr - cr)) / 2) + nb
                columnScanStart = nc - int((abs(nc - cc) + (nc - cc)) / 2) + cb
                columnScanEnd = cc + int((abs(nc - cc) + (nc - cc)) / 2) + cb
                for r in range(rowScanStart, rowScanEnd):
                    for c in range(columnScanStart, columnScanEnd):
                        if abs(c - columnScanStart) == abs(r - rowScanStart):
                            if not str(board.square(r, c)).isspace():
                                if board.square(r, c).team == self.team:
                                    return False
                                else:
                                    if r != nr or c != nc:
                                        return False
                return True
            else:
                return False
        else:
            return False
