from Piece import Piece


class King(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if board.validIndex(nr, nc):
            if abs(nc - cc) > 1 or abs(nr - cr) > 1:
                return False
            else:
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
