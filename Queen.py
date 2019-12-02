from Piece import Piece


class Queen(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        # when moving diagonally will use bishop movement code, otherwise will use rook movement code
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
                if nr != cr and nc == cc:
                    if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                        nb = 1
                        cb = 1
                    else:
                        nb = 0
                        cb = 0
                    for r in range(nr - int((abs(nr - cr) + (nr - cr)) / 2) + nb, cr + int((abs(nr - cr) + (nr - cr)) / 2) + cb):
                        if not str(board.square(r, cc)).isspace():
                            if r != nr:
                                return False
                            else:
                                if board.square(r, cc).team == self.team:
                                    return False
                    return True
                elif nc != cc and nr == cr:
                    if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                        nb = 1
                        cb = 1
                    else:
                        nb = 0
                        cb = 0
                    for c in range(nc - int((abs(nc - cc) + (nc - cc)) / 2) + nb, cc + int((abs(nc - cc) + (nc - cc)) / 2) + cb):
                        if not str(board.square(cr, c)).isspace():
                            if c != nc:
                                return False
                            else:
                                if board.square(cr, c).team == self.team:
                                    return False
                    return True
        else:
            return False
