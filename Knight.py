from Piece import Piece


class Knight(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team, 3.0)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if cc == nc or cr == nr:
            return False
        if abs(nr - cr) + abs(nc - cc) != 3:
            return False
        else:
            if str(board[nr][nc]).isspace():
                return True
            else:
                if board[nr][nc].team != self.team:
                    return True
                else:
                    return False
