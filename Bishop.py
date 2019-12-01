from Piece import Piece


class Bishop(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if board.validIndex(nr, nc):
            if nc != cc and nr != cr:
                if abs(nr - cr) == abs(nc - cc):
                    if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                        nb = 0
                        cb = 1
                    else:
                        nb = 1
                        cb = 0
                    if abs(nc - cc) == 1:
                        if not str(board.square(nr, nc)).isspace():
                            if board.square(nr, nc).team != self.team:
                                return True
                            else:
                                return False
                    for r in range(nr - int((abs(nr - cr) + (nr - cr)) / 2) + nb, cr + int((abs(nr - cr) + (nr - cr)) / 2) + cb):
                        c = int(cc + ((nc - cc) / abs(nc - cc)) * abs(r - cr))  # c equals current column plus unit vector of total column
                        # movement times the number of rows already examined, and it refers to the column that must be
                        # examined on this particular cycle
                        if not str(board.square(r, c)).isspace():
                            if r == nr and board.square(r, c).team != self.team:
                                return True
                            else:
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
            else:
                return False
        else:
            return False
