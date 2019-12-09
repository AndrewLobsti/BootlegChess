import pickle
import Pawn
import Rook
import Knight
import Bishop
import Queen
import King
import time
import cProfile


class Board:

    def __init__(self):
        self.board = []
        self.team0Moves = []
        self.team1Moves = []
        self.PiecesOnBoard = []
        self.shadowRealm = []
        self.teamInCheck = 2
        self.winningTeam = 2
        self.Castled = False
        self.enemyMovesDatabase = []
        self.responseMovesDatabase = []
        self.movePerformedByEnemy = []

    def boardConstructor(self):
        self.board.clear()
        for r in range(8):
            row = []
            for c in range(8):
                row.append(" ")
            self.board.append(row)

    def displayBoard(self):
        print("X    1    2    3    4    5    6    7    8")
        rn = 1
        for r in self.board:
            print(str(rn) + "  " + str(r))
            rn += 1

    def square(self, r, c):
        return self.board[r][c]

    def boardReplace(self, p, o, cr, cc, nr, nc):
        self.board[nr][nc] = p
        # self.board[nr].pop(nc)
        # self.board[nr].insert(nc, p)
        self.board[cr][cc] = o

    def validIndex(self, r, c):
        return 8 > r >= 0 and 8 > c >= 0

    def availablePicks(self, team):
        availablePicks = []
        for p in self.PiecesOnBoard:
            if p.team == team:
                i = [p.r, p.c]
                availablePicks.append(i)
        return availablePicks

    def kingInCheck(self, team, future):
        k = self.getKing(team + 1 - 2 * team)
        if k != 1:
            for i in self.availablePicks(team):
                p = self.getPiece(i[0], i[1], team)
                if p.validMove(self.PiecesOnBoard, k.r, k.c):
                    return True
            return False
        else:
            return True

    def getKing(self, team):
        for p in self.PiecesOnBoard:
            if p.type == "k" and p.team == team:
                return p
        return 1

    def inAttackRange(self, team):
        positions = []
        for i in self.availablePicks(team):
            ap = self.getPiece(i[0], i[1], team)
            l = self.inRange(ap, team)
            for x in l:
                positions.append(x)
        return positions

    def isAttackable(self, r, c, team):
        p = [r, c]
        for i in self.availablePicks(team):
            ap = self.getPiece(i[0], i[1], team)
            l = self.inRange(ap, team)
            if l.count(p) > 0:
                return True
        return False

    def inCheckRange(self, p, r, c, team):
        nr = 0
        for nrl in self.board:
            nc = 0
            for nce in nrl:
                if not str(nce).isspace():
                    if p.validMove(self.board, r, c, nr, nc) is True and self.square(nr, nc).team != team and self.square(nr, nc).type == "k":
                        return True
                nc += 1
            nr += 1
        return False

    def castlingCheck(self, k, team):
        kc = k.c
        if self.getPiece(k.r, k.c + 3, team) != -1:
            k.c = k.c + 1
        else:
            k.c = k.c - 1
        if self.kingInCheck(team + 1 - 2 * team, False):
            k.c = kc
            return False
        k.c = kc
        return True

    def scanRange(self, p):
        sr = [0, 8, 0, 8]
        if p.type == "p":
            rsr = 2
            sr[2] = p.c - 1
            sr[3] = p.c + 2
            if p.neverMoved:
                rsr = 3
            if p.ds == 1:
                sr[0] = p.r
                sr[1] = p.r + rsr
            else:
                sr[0] = p.r - rsr + 1
                sr[1] = p.r + 1
        elif p.type == "h":
            sr[0] = p.r - 2
            sr[1] = p.r + 3
            sr[2] = p.c - 2
            sr[3] = p.c + 3
        elif p.type == "k":
            sr[0] = p.r - 1
            sr[1] = p.r + 2
            sr[2] = p.c - 1
            sr[3] = p.c + 2
        for i in range(0, len(sr)):
            if sr[i] < 0:
                sr[i] = 0
            elif sr[i] > 8:
                sr[i] = 8
        return sr

    def inRange(self, p, team):
        inRange = []
        sr = self.scanRange(p)
        for r in range(sr[0], sr[1]):
            for c in range(sr[2], sr[3]):
                if p.validMove(self.PiecesOnBoard, r, c):
                    append = True
                    if p.type == "k":
                        if abs(p.c - c) > 1:
                            if not self.castlingCheck(p, team):
                                append = False
                    pr = p.r
                    pc = p.c
                    p.r = r
                    p.c = c
                    if self.kingInCheck(team + 1 - 2 * team, False):
                        append = False
                    p.r = pr
                    p.c = pc
                    if append:
                        square = [r, c]
                        inRange.append(square)
        return inRange

    def getPiece(self, r, c, team):
        for p in self.PiecesOnBoard:
            if p.r == r and p.c == c and p.team == team:
                return p
        return 1

    def movePiece(self, p, nr, nc):
        np = self.getPiece(nr, nc, p.team + 1 - 2 * p.team)
        cr = p.r
        cc = p.c
        p.neverMoved = False
        p.moves += 1
        if np != 1:
            # print(str(cp) + " just ate " + str(np) + " !")
            self.shadowRealm.append(np)
            self.PiecesOnBoard.remove(np)
            self.boardReplace(p.ID, " ", cr, cc, nr, nc)
            p.r = nr
            p.c = nc
        elif p.type == "p" and nc != cc:
            pp = self.getPiece(cr, nc, p.team + 1 - 2 * p.team)
            # print(str(cp) + " just ate " + str(pp) + " !")
            # print("er passant!")
            self.shadowRealm.append(pp)
            self.PiecesOnBoard.remove(pp)
            self.boardReplace(p.ID, " ", cr, cc, nr, nc)
            self.board[cr][nc] = " "
            p.r = nr
            p.c = nc
        else:
            self.boardReplace(p.ID, " ", cr, cc, nr, nc)
            p.r = nr
            p.c = nc
        self.teamInCheck = 2
        if self.kingInCheck(0, False):
            self.teamInCheck = 1
            # print("1 in check!")
        elif self.kingInCheck(1, False):
            self.teamInCheck = 0
            # print("0 in check!")

    def promotePawn(self, r, c, team, AI):
        while True:
            p = "p"
            if AI == 0:
                p = str(input())
                p = p.lower()
            elif AI == 1:
                pass
            elif AI == 2:
                self.PiecesOnBoard.remove(self.getPiece(r, c, team))
                pp = Queen.Queen("q", team, r, c)
                self.board[r].pop(c)
                self.board[r].insert(c, pp.ID)
                self.PiecesOnBoard.append(pp)
                break
            self.board[r].pop(c)
            if p == "q":
                self.PiecesOnBoard.remove(self.getPiece(r, c, team))
                pp = Queen.Queen("q", team, r, c)
                self.board[r].pop(c)
                self.board[r].insert(c, pp.ID)
                self.PiecesOnBoard.append(pp)
                break
            elif p == "h":
                self.PiecesOnBoard.remove(self.getPiece(r, c, team))
                pp = Knight.Knight("h", team, r, c)
                self.board[r].pop(c)
                self.board[r].insert(c, pp.ID)
                self.PiecesOnBoard.append(pp)
                break
            elif p == "r":
                self.PiecesOnBoard.remove(self.getPiece(r, c, team))
                pp = Rook.Rook("r", team, r, c)
                self.board[r].pop(c)
                self.board[r].insert(c, pp.ID)
                self.PiecesOnBoard.append(pp)
                break
            elif p == "b":
                self.PiecesOnBoard.remove(self.getPiece(r, c, team))
                pp = Bishop.Bishop("b", team, r, c)
                self.board[r].pop(c)
                self.board[r].insert(c, pp.ID)
                self.PiecesOnBoard.append(pp)
                break

    def addtoMovementList(self, y, np, p, t):
        if t == 0:
            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
            self.team0Moves.append(move)
        else:
            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
            self.team1Moves.append(move)

    def bigBrainTime(self, team, IQ):
        bestPlay = ["X", 0, 0, 0, 0, 0.0, 0]
        playValue = 0.0
        bestValue = -2000.0
        if IQ > 0:
            et = team + 1 - 2 * team
            a = self.availablePicks(team)
            for y in a:
                playValue = 0.0
                p = self.getPiece(y[0], y[1], team)
                if p != 1:
                    m = self.inRange(p, team)
                else:
                    m = []
                if len(m) > 0:
                    for i in m:
                        appendS = False
                        playValue = 0.0
                        s = None
                        if self.availablePicks(et).count(i) > 0:
                            s = self.getPiece(i[0], i[1], et)
                            playValue += s.value
                            self.PiecesOnBoard.remove(s)
                            appendS = True
                        pr = p.r
                        pc = p.c
                        p.r = i[0]
                        p.c = i[1]
                        # self.boardReplace(p.ID, " ", y[0], y[1], i[0], i[1])
                        for ep in self.availablePicks(et):
                            e = self.getPiece(ep[0], ep[1], et)
                            em = self.inRange(e, et)
                            if len(em) > 0:
                                friendlyDeadPieces = []
                                for ei in em:
                                    willDie = False
                                    er = e.r
                                    ec = e.c
                                    e.r = ei[0]
                                    e.c = ei[1]
                                    if self.availablePicks(team).count(ei) > 0:
                                        ftp = self.getPiece(ei[0], ei[1], team)  # friendly team piece
                                        if friendlyDeadPieces.count(ftp) == 0:
                                            playValue -= ftp.value
                                            friendlyDeadPieces.append(ftp)
                                            self.PiecesOnBoard.remove(ftp)
                                            if IQ - 1 > 0:
                                                futureBestPlay = self.bigBrainTime(team, IQ - 1)
                                                playValue += futureBestPlay[5]
                                                self.enemyMovesDatabase.append(ei)
                                                self.responseMovesDatabase.append(futureBestPlay)
                                            self.PiecesOnBoard.append(ftp)
                                        elif IQ - 1 > 0:
                                                futureBestPlay = self.bigBrainTime(team, IQ - 1)
                                                playValue += futureBestPlay[5]
                                                self.enemyMovesDatabase.append(ei)
                                                self.responseMovesDatabase.append(futureBestPlay)
                                    elif IQ - 1 > 0:
                                        futureBestPlay = self.bigBrainTime(team, IQ - 1)
                                        playValue += futureBestPlay[5]
                                        self.enemyMovesDatabase.append(ei)
                                        self.responseMovesDatabase.append(futureBestPlay)
                                    e.r = er
                                    e.c = ec
                        if playValue >= bestValue:
                            bestValue = playValue
                            bestPlay[0] = p
                            bestPlay[1] = y[0]
                            bestPlay[2] = y[1]
                            bestPlay[3] = i[0]
                            bestPlay[4] = i[1]
                            bestPlay[5] = bestValue
                        p.r = pr
                        p.c = pc
                        if appendS:
                            self.PiecesOnBoard.append(s)
                        # self.boardReplace(str(s), p.ID, y[0], y[1], i[0], i[1])
            # print(playValue)
            # print(bestValue)
            # print(bestPlay)
            if bestValue < -500.0:
                self.winningTeam = et
        return bestPlay

    def GLadOSX(self, team):
        t = team + 1 - 2 * team
        self.Castled = False
        # cProfile.runctx('self.bigBrainTime(t, 2)', globals(), locals())
        # if len(self.responseMovesDatabase) > 0:
            # i = self.enemyMovesDatabase.index(self.movePerformedByEnemy[0])
            # bestPlay = self.responseMovesDatabase[i]
            # self.responseMovesDatabase.clear()
            # self.movePerformedByEnemy.clear()
        # else:
        bestPlay = self.bigBrainTime(t, 2)
        p = bestPlay[0]
        cr = bestPlay[1]
        cc = bestPlay[2]
        nr = bestPlay[3]
        nc = bestPlay[4]
        if p.type == "p":
            self.movePiece(p, nr, nc)
            if p.promotionRow == nr:
                self.promotePawn(nr, nc, t, 2)
        elif p.type == "k":
            if abs(nc - p.c) > 1:
                print("Castling!")
                self.Castled = True
                if nc - cc < 0:
                    self.movePiece(self.getPiece(cr, cc - 4, t), nr, nc + 1)
                else:
                    self.movePiece(self.getPiece(cr, cc + 3, t), nr, nc + 1)
            else:
                self.movePiece(p, nr, nc)

        else:
            self.movePiece(p, nr, nc)

    def Wheatley(self, team):
        pass

    def playerTurn(self, team):
        player = "Lowercase"
        if team == 1:
            player = "Uppercase"
        possiblePicks = []
        for x in self.availablePicks(team):
            p = self.getPiece(x[0], x[1], team)
            possibleMoves = self.inRange(p, team)
            if len(possibleMoves) > 0:
                possiblePicks.append(p)
        if len(possiblePicks) > 0:
            while True:
                print(
                    player + " pieces player, choose the row and column where the piece you wish to move is located! (both values must be >= 1 and <= 8")
                r = int(input()) - 1
                c = int(input()) - 1
                cp = [r, c]
                if self.availablePicks(team).count(cp) > 0:
                    p = self.getPiece(r, c, team)
                    inRange = self.inRange(p, team)
                    print("you selected the " + str(p) + " in row " + str(r) + " and column" + str(c))
                    print(
                        "please input the row and column where the position you want to move it to is located. If you dont want to move this piece, input 0 and 0")
                    nr = int(input()) - 1
                    nc = int(input()) - 1
                    np = [nr, nc]
                    if inRange.count(np) > 0:
                        if p.type == "p":
                            if p.promotionRow == nr:
                                print("Your pawn reached the promotion row, as such you must now promote it! type the symbol of a piece of your choice (except pawns or kings) to replace the pawn with it")
                                self.movePiece(p, nr, nc)
                                self.movePerformedByEnemy.append(np)
                                self.promotePawn(nr, nc, team, 0)
                                break
                        if p.type == "k":
                            if abs(nc - c) > 1:
                                if nc - c < 0:
                                    self.movePiece(self.getPiece(r, c - 4, team), nr, nc + 1)
                                else:
                                    self.movePiece(self.getPiece(r, c + 3, team), nr, nc + 1)
                        self.movePiece(p, nr, nc)
                        self.movePerformedByEnemy.append(np)
                        break
                    else:
                        print("error: that was not a position your piece could move to!")
                else:
                    print("That position does not have a piece you can pick! please select another position")
        else:
            self.winningTeam = team + 1 - 2 * team

    def piecesOnBoard(self):
        n = 0
        for r in range(1, 9):
            for c in range(1, 9):
                if not str(self.square(r, c)).isspace():
                    n += 1
        return n

    def saveListToFile(self, t, m):
        if t == 0:
            l = self.team0Moves
            fn = m + "team0Moves"
            f = open(fn, "wb")
            pickle.dump(l, f)
            f.close()
        elif t == 1:
            l = self.team1Moves
            fn = m + "team1Moves"
            f = open(fn, "wb")
            pickle.dump(l, f)
            f.close()

    def gameStart(self):
        print("CHESS MEGA")
        print("Pieces are denoted my letters, lowercases and uppers. Lowercases move first! now select yours: input 0 "
              "for the lowercases or "
              "1 for uppers, and then press enter. Note: if this is "
              "to be a local multiplayer match, one player should input the team and starting position, and the other "
              "will takes the opposites.")
        team = int(input())
        if team != 0 and team != 1:
            print("your IQ is less than 8, so we selected a team for you mate")
            if team % 2 != 0:
                team = 1
            else:
                team = 0
        print("Now select your starting position: 0 for south 1 for north")
        northstart = int(input())
        if northstart != 0 and northstart != 1:
            print("Your IQ is 1000. In base 2. so we selected a start for you.")
            if northstart % 2 != 0:
                northstart = 1
            else:
                northstart = 0
        print("you can read matey, so your IQ is at least 80. You have successfully passed the entry test, "
              "and we will now setup the rest.")
        rn = 0
        enable = True
        for r in self.board:
            for c in range(0, 8):
                if rn == (1 * northstart) + 6 * (1 - northstart):
                    r.pop(c)
                    p = Pawn.Pawn("p", team, rn, c)
                    r.insert(c, p.ID)
                    self.PiecesOnBoard.append(p)
                if rn == (1 * (1 - northstart)) + 6 * northstart:
                    r.pop(c)
                    p = Pawn.Pawn("p", team + 1 - 2 * team, rn, c)
                    r.insert(c, p.ID)
                    self.PiecesOnBoard.append(p)
                if enable:
                    if rn == 0 + 7 * (1 - northstart):
                        if c == 0 or c == 7:
                            r.pop(c)
                            p = Rook.Rook("r", team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 1 or c == 6:
                            r.pop(c)
                            p = Knight.Knight("h", team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 2 or c == 5:
                            r.pop(c)
                            p = Bishop.Bishop("b", team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 3:
                            r.pop(c)
                            p = Queen.Queen("q", team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 4:
                            r.pop(c)
                            p = King.King("k", team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                    elif rn == 0 + 7 * northstart:
                        if c == 0 or c == 7:
                            r.pop(c)
                            p = Rook.Rook("r", team + 1 - 2 * team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 1 or c == 6:
                            r.pop(c)
                            p = Knight.Knight("h", team + 1 - 2 * team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 2 or c == 5:
                            r.pop(c)
                            p = Bishop.Bishop("b", team + 1 - 2 * team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 3:
                            r.pop(c)
                            p = Queen.Queen("q", team + 1 - 2 * team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
                        if c == 4:
                            r.pop(c)
                            p = King.King("k", team + 1 - 2 * team, rn, c)
                            r.insert(c, p.ID)
                            self.PiecesOnBoard.append(p)
            rn += 1
        self.displayBoard()
        while True:
            print(
                "setup complete! now select number of players: 1 for vs AI, and 2 for local multiplayer")
            np = int(input())
            if not 3 > np > 0:
                print("incorrect number inputed. Please input a correct number. The correct number to input is "
                      "one that is not incorrect")
            else:
                break
        if np == 2:
            print("Game Start! this is a multiplayer match, so each player takes turn moving their pieces.")
            while self.winningTeam == 2:
                if self.winningTeam == 2:
                    self.playerTurn(0)
                    self.displayBoard()
                if self.winningTeam == 2:
                    self.playerTurn(1)
                    self.displayBoard()
            print("team " + str(self.winningTeam) + " won the match!")
        elif np == 1:
            print(
                "Game Start! this is a vs AI match, so just input your move and then wait for your opponent, Dr Eggman, to input his!")
            while self.winningTeam == 2:
                if team == 0:
                    if self.winningTeam == 2:
                        self.playerTurn(team)
                        self.displayBoard()
                elif self.winningTeam == 2:
                    print(
                        "Dr Eggman is the Lowercase pieces player, please wait for his eggxcelency to input his move!")
                    startTime = time.perf_counter()
                    self.GLadOSX(team)
                    self.movePerformedByEnemy.clear()
                    print(time.perf_counter() - startTime)
                    self.displayBoard()
                if team == 1:
                    if self.winningTeam == 2:
                        self.playerTurn(team)
                        self.displayBoard()
                elif self.winningTeam == 2:
                    print(
                        "Dr Eggman is the Uppercase pieces player, please wait for his eggxcelency to input his move!")
                    startTime = time.perf_counter()
                    self.GLadOSX(team)
                    self.movePerformedByEnemy.clear()
                    print(time.perf_counter() - startTime)
                    self.displayBoard()
            print("team " + str(self.winningTeam) + " won the match!")


b = Board()
b.boardConstructor()
b.gameStart()
# b.trainingStats()
