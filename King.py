from Piece import Piece


class King(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team, 1000)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if abs(nr - cr) > 1:
            return False
        if board.validIndex(nr, nc):
            if abs(nc - cc) == 2:  # Castling Code
                if nr != cr or self.neverMoved is False or str(board.square(nr, nc)).isspace() is False:
                    return False
                if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                    cb = 1
                    nb = 1
                    rookColumn = cc + int((abs(nc - cc) + (nc - cc)) / 2) + nb
                else:
                    cb = -1
                    nb = 0
                    rookColumn = nc - int((abs(nc - cc) + (nc - cc)) / 2) - 2
                if str(board.square(cr, rookColumn)).isspace():
                    return False
                elif board.square(cr, rookColumn).team != self.team:
                    return False
                elif str(board.square(cr, rookColumn)) != " r " and str(board.square(cr, rookColumn)) != " R ":
                    return False
                scanStart = nc - int((abs(nc - cc) + (nc - cc)) / 2) + cb
                scanEnd = cc + int((abs(nc - cc) + (nc - cc)) / 2) + nb
                for c in range(scanStart, scanEnd):
                    if not str(board.square(cr, c)).isspace():
                        return False
                return True
            else:
                if abs(nc - cc) > 1:
                    return False
                if nc != cc and nr != cr:
                    if abs(nc - cc) != abs(nr - cr):
                        return False
                if not str(board.square(nr, nc)).isspace():
                    if board.square(nr, nc).team != self.team:
                        return True
                    else:
                        return False
                else:
                    return True
        else:
            return False
