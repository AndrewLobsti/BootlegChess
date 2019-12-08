from Piece import Piece


class Bishop(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team, 3.0)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if not str(board[nr][nc]).isspace():
            if board[nr][nc].team == self.team:
                return False
        if abs(nr - cr) == abs(nc - cc):
            if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                nb = 1
            else:
                nb = 0
            rowScanStart = nr - int((abs(nr - cr) + (nr - cr)) / 2)
            rowScanEnd = cr + int((abs(nr - cr) + (nr - cr)) / 2) + nb
            for r in range(rowScanStart, rowScanEnd):
                # for c in range(columnScanStart, columnScanEnd):
                c = int(cc + ((nc - cc) / abs(nc - cc)) * abs(r - cr))
                # if abs(c - columnScanStart) == abs(r - rowScanStart):
                if c != cc and c != nc:
                    if not str(board[r][c]).isspace():
                        if board[r][c].team == self.team:
                            return False
                        else:
                            if r != nr or c != nc:
                                return False
            return True
        else:
            return False
