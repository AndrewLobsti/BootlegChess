from Piece import Piece


class Rook(Piece):

    def __init__(self, ID, team):
        super().__init__(ID, team)

    # noinspection PyAttributeOutsideInit
    def validMove(self, board, cr, cc, nr, nc):
        if nr == cr and nc == cc:
            return False
        if board.validIndex(nr, nc):
            if nr != cr and nc != cc:
                return False
            if nr != cr:
                if int((abs(nr - cr) + (nr - cr)) / 2) != 0:
                    nb = 1
                    cb = 1
                else:
                    nb = 0
                    cb = 0
                for r in range(nr - int((abs(nr-cr) + (nr-cr)) / 2) + nb, cr + int((abs(nr - cr) + (nr - cr)) / 2) + cb):
                    # this will cycle over the rows that are between where the piece is and where we want it to be.
                    # the math inside the range function will compute the number of lines (nr - cr) we add (cr +) or
                    # subtract (nr -) to go from our current row (cr) to the row we want to move to (nr, next row),
                    # or vice-versa, and will then add the distance (abs(nr - cr)) from cr to nr. It will then divide
                    # the computed value by 2. By doing this, our for function will always cycle from the smallest to
                    # biggest row, no matter the direction we want to move in, since if the first argument in the
                    # range function is to be nr then it means nr < cr, and our computation will do either nr - 0/2
                    # or cr + 0/2, and vice-versa if the first argument is to be cr. This is to be used for vertical
                    # movement.
                    if not str(board.square(r, cc)).isspace():
                        if r != nr:
                            return False
                        else:
                            if board.square(r, cc).team == self.team:
                                return False
                return True
            else:
                if int((abs(nc - cc) + (nc - cc)) / 2) != 0:
                    nb = 1
                    cb = 1
                else:
                    nb = 0
                    cb = 0
                for c in range(nc - int((abs(nc-cc) + (nc-cc)) / 2) + nb, cc + int((abs(nc - cc) + (nc - cc)) / 2) + cb):
                    # same as explained in the comment bloc above, but for lengthwise movement.
                    if not str(board.square(cr, c)).isspace():
                        if c != nc:
                            return False
                        else:
                            if board.square(cr, c).team == self.team:
                                return False
                return True
        else:
            return False

