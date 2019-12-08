from Piece import Piece


class King(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team, 1000.0)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if abs(nr - cr) > 1:
            return False
        if abs(nc - cc) == 2:  # Castling Code
            if nr != cr or self.neverMoved is False or str(board[nr][nc]).isspace() is False:
                return False
            if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                rookColumn = 7
                scanStart = cc + 1
                scanEnd = 8
            else:
                rookColumn = 0
                scanStart = 2
                scanEnd = cc
            if str(board[nr][rookColumn]).isspace():
                return False
            elif board[nr][rookColumn].team != self.team:
                return False
            elif board[nr][rookColumn].type != "r":
                return False
            for c in range(scanStart, scanEnd):
                if not str(board[cr][c]).isspace():
                    return False
            return True
        else:
            if abs(nc - cc) > 1:
                return False
            if nc != cc and nr != cr:
                if abs(nc - cc) != abs(nr - cr):
                    return False
            if not str(board[nr][nc]).isspace():
                if board[nr][nc].team != self.team:
                    return True
                else:
                    return False
            else:
                return True
