import random
import pickle
import Pawn
import Rook
import Knight
import Bishop
import Queen
import King
import time


class Board:

    def __init__(self):
        self.board = []
        self.team0Moves = []
        self.team1Moves = []
        self.shadowRealm = []
        self.teamInCheck = 2
        self.winningTeam = 2
        self.Castled = False

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
        r = 0
        for rl in self.board:
            c = 0
            for ce in rl:
                p = ce
                if not str(p).isspace():
                    if p.team == team:
                        i = [r, c]
                        availablePicks.append(i)
                c += 1
            r += 1
        return availablePicks

    def kingInCheck(self, team, future):
        for i in self.availablePicks(team):
            p = self.square(i[0], i[1])
            r = 0
            for rl in self.board:
                c = 0
                for ce in rl:
                    if p.validMove(self.board, i[0], i[1], r, c):
                        if str(ce) == " k " or str(ce) == " K ":
                            # if not future:
                            # print(str(p) + " in " + str(i[0]) + "," + str(i[1]) + " has the enemy team in check!")
                            # print(self.inRange(p, i[0], i[1], team))
                            return True
                    c += 1
                r += 1
        return False

    def inAttackRange(self, team):
        positions = []
        for i in self.availablePicks(team):
            ap = self.getPiece(i[0], i[1], team)
            l = self.inRange(ap, i[0], i[1], team)
            for x in l:
                positions.append(x)
        return positions

    def isAttackable(self, r, c, team):
        p = [r, c]
        for i in self.availablePicks(team):
            ap = self.getPiece(i[0], i[1], team)
            l = self.inRange(ap, i[0], i[1], team)
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

    def inRange(self, p, cr, cc, team):
        inRange = []
        r = 0
        for rl in self.board:
            c = 0
            for ce in rl:
                if p.validMove(self.board, cr, cc, r, c):
                    nc = c
                    append = True
                    if p.type == "k":  # not castling trough check check
                        if abs(c - cc) > 1:
                            if self.kingInCheck(team + 1 - 2 * team, False):
                                append = False
                            self.boardReplace(p, " ", cr, cc, r, nc)
                            if self.kingInCheck(team + 1 - 2 * team, True):
                                append = False
                            self.boardReplace(ce, p, cr, cc, r, nc)
                            if (c - cc) < 0:
                                nc = c + 1
                            else:
                                nc = c - 1
                    self.boardReplace(p, " ", cr, cc, r, nc)
                    if not self.kingInCheck(team + 1 - 2 * team, True):
                        if append:
                            square = [r, c]
                            inRange.append(square)
                    self.boardReplace(ce, p, cr, cc, r, nc)
                c += 1
            r += 1
        return inRange

    def getPiece(self, r, c, team):
        s = str(self.square(r, c))
        if not s.isspace():
            p = self.square(r, c)
            if p.team == team:
                return p
            else:
                return 1
        else:
            return 1

    def movePiece(self, cr, cc, nr, nc):
        np = self.square(nr, nc)
        cp = self.square(cr, cc)
        cp.neverMoved = False
        cp.moves += 1
        if not str(np).isspace():
            # print(str(cp) + " just ate " + str(np) + " !")
            self.shadowRealm.append(np)
            self.boardReplace(cp, " ", cr, cc, nr, nc)
        elif cp.type == "p" and nc != cc:
            pp = self.square(cr, nc)
            # print(str(cp) + " just ate " + str(pp) + " !")
            # print("er passant!")
            self.shadowRealm.append(pp)
            self.boardReplace(cp, " ", cr, cc, nr, nc)
            self.board[cr][nc] = " "
        else:
            self.boardReplace(cp, " ", cr, cc, nr, nc)
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
                # noinspection PyListCreation
                pp = []
                pp.append(Queen.Queen("q", team))
                pp.append(Knight.Knight("h", team))
                pp.append(Rook.Rook("r", team))
                pp.append(Bishop.Bishop("b", team))
                p = random.randint(0, 3)
                # print("Pawn promoted to " + str(pp[p]) + " !")
                self.board[r].pop(c)
                self.board[r].insert(c, pp[p])
                break
            elif AI == 2:
                pp = Queen.Queen("q", team)
                self.board[r].pop(c)
                self.board[r].insert(c, pp)
                break
            self.board[r].pop(c)
            if p == "q":
                self.board[r].insert(c, Queen.Queen(p, team))
                break
            elif p == "h":
                self.board[r].insert(c, Knight.Knight(p, team))
                break
            elif p == "r":
                self.board[r].insert(c, Rook.Rook(p, team))
                break
            elif p == "b":
                self.board[r].insert(c, Bishop.Bishop(p, team))
                break

    def addtoMovementList(self, y, np, p, t):
        if t == 0:
            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
            self.team0Moves.append(move)
        else:
            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
            self.team1Moves.append(move)

    def bigBrainTime(self, team, IQ):
        bestPlay = [None, 0, 0, 0, 0, 0]
        playValue = 0.0
        bestValue = 0.0
        if IQ > 0:
            et = team + 1 - 2 * team
            a = self.availablePicks(team)
            piecesInDanger = self.inAttackRange(et)
            for x in a:
                y = self.getPiece(x[0], x[1], team)
                if piecesInDanger.count(x) > 0:
                    bestValue -= y.value
            for y in a:
                playValue = 0.0
                p = self.getPiece(y[0], y[1], team)
                m = self.inRange(p, y[0], y[1], team)
                if len(m) > 0:
                    for i in m:
                        playValue = 0.0
                        if self.availablePicks(et).count(i) > 0:
                            playValue += self.getPiece(i[0], i[1], et).value
                        s = self.square(i[0], i[1])
                        self.boardReplace(p, " ", y[0], y[1], i[0], i[1])
                        for ep in self.availablePicks(et):
                            e = self.getPiece(ep[0], ep[1], et)
                            em = self.inRange(e, ep[0], ep[1], et)
                            if len(em) > 0:
                                for ei in em:
                                    if self.availablePicks(team).count(ei) > 0:
                                        playValue -= self.getPiece(ei[0], ei[1], team).value
                        futureBestPlay = self.bigBrainTime(team, IQ - 1)
                        playValue += futureBestPlay[5]
                        if playValue >= bestValue:
                            bestValue = playValue
                            bestPlay[0] = p
                            bestPlay[1] = y[0]
                            bestPlay[2] = y[1]
                            bestPlay[3] = i[0]
                            bestPlay[4] = i[1]
                            bestPlay[5] = bestValue
                        self.boardReplace(s, p, y[0], y[1], i[0], i[1])
            # print(playValue)
            # print(bestValue)
            # print(bestPlay)
            if bestValue < -500.0:
                self.winningTeam = et
        return bestPlay

    # noinspection PyUnusedLocal
    def chooseMove(self, possibleMoves, team):
        bestPlay = [None, 0, 0, 0, 0]
        playValue = 0.0
        bestValue = 0.0
        piecesInDanger = self.inAttackRange(team + 1 - 2 * team)
        for x in self.availablePicks(team):
            y = self.getPiece(x[0], x[1], team)
            if piecesInDanger.count(x) > 0:
                bestValue -= y.value
        piecesInDanger = self.inAttackRange(team + 1 - 2 * team)
        for i in possibleMoves:
            playValue = 0.0
            p = self.getPiece(i[0], i[1], team)
            movementChoices = self.inRange(p, i[0], i[1], team)
            for m in movementChoices:
                playValue = 0.0
                s = self.square(m[0], m[1])
                self.boardReplace(p, " ", i[0], i[1], m[0], m[1])
                willBeInDanger = self.isAttackable(m[0], m[1], team + 1 - 2 * team)
                piecesThatWillBeInDanger = self.inAttackRange(team + 1 - 2 * team)
                piecesThatWillBeAttackable = self.inAttackRange(team)
                for x in self.availablePicks(team):
                    y = self.getPiece(x[0], x[1], team)
                    if piecesThatWillBeInDanger.count(x) > 0:
                        playValue -= y.value
                for x in piecesThatWillBeAttackable:
                    y = self.getPiece(x[0], x[1], team + 1 - 2 * team)
                    if y != 1 and willBeInDanger is False:
                        playValue += y.value * 0.05
                # self.chooseMove(possibleMovements, team, IQ - 1)
                self.boardReplace(s, p, i[0], i[1], m[0], m[1])
                inDanger = self.isAttackable(i[0], i[1], team + 1 - 2 * team)
                if p.type == "p":
                    if p.promotionRow == m[0] and willBeInDanger is False:
                        playValue += 9.0  # worth of a Queen
                if not str(self.square(m[0], m[1])).isspace():
                    ep = self.square(m[0], m[1])
                    playValue += ep.value
                    if inDanger:
                        playValue += p.value
                elif inDanger:
                    playValue += p.value
                if self.inCheckRange(p, m[0], m[1], team) and willBeInDanger is False:
                    playValue += 2.0
                if playValue >= bestValue:
                    bestValue = playValue
                    bestPlay[0] = p
                    bestPlay[1] = i[0]
                    bestPlay[2] = i[1]
                    bestPlay[3] = m[0]
                    bestPlay[4] = m[1]
        print(playValue)
        print(bestValue)
        print(bestPlay)
        return bestPlay

    def GLadOSX(self, team):
        t = team + 1 - 2 * team
        self.Castled = False
        bestPlay = self.bigBrainTime(t, 2)
        p = bestPlay[0]
        cr = bestPlay[1]
        cc = bestPlay[2]
        nr = bestPlay[3]
        nc = bestPlay[4]
        if str(p) == " p " or str(p) == " P ":
            self.movePiece(cr, cc, nr, nc)
            if p.promotionRow == nr:
                self.promotePawn(nr, nc, t, 2)
        elif str(p) == " k " or str(p) == " K ":
            if abs(nc - cc) > 1:
                print("Castling!")
                self.Castled = True
                if nc - cc < 0:
                    self.movePiece(cr, cc - 4, nr, nc + 1)
                else:
                    self.movePiece(cr, cc + 3, nr, nc - 1)
            else:
                self.movePiece(cr, cc, nr, nc)
        else:
            self.movePiece(cr, cc, nr, nc)

    def GLadOS(self, team):
        t = team + 1 - 2 * team
        self.Castled = False
        possibleMovements = []
        a = self.availablePicks(t)
        s = len(a)
        for x in range(s):
            y = a[x]
            p = self.getPiece(y[0], y[1], t)
            e = self.inRange(p, y[0], y[1], t)
            if len(e) > 0:
                possibleMovements.append(y)
        length = len(possibleMovements)
        if length > 0:
            bestPlay = self.chooseMove(possibleMovements, t)
            p = bestPlay[0]
            cr = bestPlay[1]
            cc = bestPlay[2]
            nr = bestPlay[3]
            nc = bestPlay[4]
            if str(p) == " p " or str(p) == " P ":
                self.movePiece(cr, cc, nr, nc)
                if p.promotionRow == nr:
                    self.promotePawn(nr, nc, t, 2)
            elif str(p) == " k " or str(p) == " K ":
                if abs(nc - cc) > 1:
                    print("Castling!")
                    self.Castled = True
                    if nc - cc < 0:
                        self.movePiece(cr, cc - 4, nr, nc + 1)
                    else:
                        self.movePiece(cr, cc + 3, nr, nc - 1)
                else:
                    self.movePiece(cr, cc, nr, nc)
            else:
                self.movePiece(cr, cc, nr, nc)
        else:
            self.winningTeam = team

    def Wheatley(self, team):
        t = team + 1 - 2 * team
        self.Castled = False
        possibleMovements = []
        a = self.availablePicks(t)
        s = len(a)
        for x in range(s):
            y = a[x]
            p = self.getPiece(y[0], y[1], t)
            e = self.inRange(p, y[0], y[1], t)
            if len(e) > 0:
                possibleMovements.append(y)
        length = len(possibleMovements)
        if length > 0:
            if length - 1 > 0:
                y = possibleMovements[random.randint(0, length - 1)]
            else:
                y = possibleMovements[0]
            p = self.getPiece(y[0], y[1], t)
            length = len(self.inRange(p, y[0], y[1], t))
            if length - 1 > 0:
                np = self.inRange(p, y[0], y[1], t)[random.randint(0, length - 1)]
            else:
                np = self.inRange(p, y[0], y[1], t)[0]
            if str(p) == " p " or str(p) == " P ":
                self.movePiece(y[0], y[1], np[0], np[1])
                if p.promotionRow == np[0]:
                    self.promotePawn(np[0], np[1], t, 1)
                self.addtoMovementList(y, np, p, t)
            elif str(p) == " k " or str(p) == " K ":
                if abs(np[1] - y[1]) > 1:
                    print("Castling!")
                    self.Castled = True
                    if np[1] - y[1] < 0:
                        self.movePiece(y[0], y[1] - 4, np[0], np[1] + 1)
                    else:
                        self.movePiece(y[0], y[1] + 3, np[0], np[1] - 1)
                else:
                    self.movePiece(y[0], y[1], np[0], np[1])
            else:
                self.movePiece(y[0], y[1], np[0], np[1])
                self.addtoMovementList(y, np, p, t)
        else:
            self.winningTeam = team

    def playerTurn(self, team):
        player = "Lowercase"
        if team == 1:
            player = "Uppercase"
        possiblePicks = []
        for x in self.availablePicks(team):
            p = self.getPiece(x[0], x[1], team)
            possibleMoves = self.inRange(p, x[0], x[1], team)
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
                    inRange = self.inRange(p, r, c, team)
                    print("you selected the " + str(p) + " in row " + str(r) + " and column" + str(c))
                    print(
                        "please input the row and column where the position you want to move it to is located. If you dont want to move this piece, input 0 and 0")
                    nr = int(input()) - 1
                    nc = int(input()) - 1
                    np = [nr, nc]
                    if inRange.count(np) > 0:
                        if p.type == "p":
                            if p.promotionRow == nr:
                                print(
                                    "Your pawn reached the promotion row, as such you must now promote it! type the symbol of a piece of your choice (except pawns or kings) to replace the pawn with it")
                                self.movePiece(r, c, nr, nc)
                                self.promotePawn(nr, nc, team, 0)
                                break
                        if p.type == "k":
                            if abs(nc - c) > 1:
                                if nc - c < 0:
                                    self.movePiece(r, c - 4, nr, nc + 1)
                                else:
                                    self.movePiece(r, c + 3, nr, nc - 1)
                        self.movePiece(r, c, nr, nc)
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

    def spartanTrainingFacility(self):
        match = 300
        while match < 600:
            self.winningTeam = 2
            self.boardConstructor()
            self.team0Moves.clear()
            self.team1Moves.clear()
            self.shadowRealm.clear()
            team = random.randint(0, 1)
            northstart = random.randint(0, 1)
            enable = True
            for r in self.board:
                for c in range(1, 9):
                    if r[0] == str((2 * northstart) + 7 * (1 - northstart)):
                        r.pop(c)
                        r.insert(c, Pawn.Pawn("p", team, (2 * northstart) + 7 * (1 - northstart)))
                    elif r[0] == str(2 + 5 * northstart):
                        r.pop(c)
                        r.insert(c, Pawn.Pawn("p", team + 1 - 2 * team, 2 + 5 * northstart))
                    if enable:
                        if r[0] == str((1 * northstart) + 8 * (1 - northstart)):
                            if c == 1 or c == 8:
                                r.pop(c)
                                r.insert(c, Rook.Rook("r", team))
                            if c == 2 or c == 7:
                                r.pop(c)
                                r.insert(c, Knight.Knight("h", team))
                            if c == 3 or c == 6:
                                r.pop(c)
                                r.insert(c, Bishop.Bishop("b", team))
                            if c == 4:
                                r.pop(c)
                                r.insert(c, Queen.Queen("q", team))
                            if c == 5:
                                r.pop(c)
                                r.insert(c, King.King("k", team))
                        elif r[0] == str(1 + 7 * northstart):
                            if c == 1 or c == 8:
                                r.pop(c)
                                r.insert(c, Rook.Rook("r", team + 1 - 2 * team))
                            if c == 2 or c == 7:
                                r.pop(c)
                                r.insert(c, Knight.Knight("h", team + 1 - 2 * team))
                            if c == 3 or c == 6:
                                r.pop(c)
                                r.insert(c, Bishop.Bishop("b", team + 1 - 2 * team))
                            if c == 4:
                                r.pop(c)
                                r.insert(c, Queen.Queen("q", team + 1 - 2 * team))
                            if c == 5:
                                r.pop(c)
                                r.insert(c, King.King("k", team + 1 - 2 * team))
            turns = 0
            pr = self.piecesOnBoard()
            while turns < 500 and pr > 3 and self.winningTeam == 2:
                if self.winningTeam == 2:
                    self.Wheatley(1)
                    # print(self.team0Moves)
                    # self.displayBoard()
                turns += 1
                if self.winningTeam == 2:
                    self.GLadOS(0)
                    # print(self.team1Moves)
                    # self.displayBoard()
                turns += 1
                pr = self.piecesOnBoard()
            if str(self.winningTeam) == str(0):
                print("team " + str(self.winningTeam) + " won the match in " + str(turns) + " moves")
                # self.kingInCheck(0, False)
                print(self.shadowRealm)
                self.displayBoard()
                # self.saveListToFile(0, str(match))
                match += 1
            elif str(self.winningTeam) == str(1):
                print("team " + str(self.winningTeam) + " won the match in " + str(turns) + " moves")
                # self.kingInCheck(1, False)
                print(self.shadowRealm)
                self.displayBoard()
                # self.saveListToFile(1, str(match))
                match += 1
            else:
                print("draw in " + str(turns) + " moves")
                print(self.shadowRealm)
                self.displayBoard()

    def trainingStats(self):
        lowerWins = 0
        upperWins = 0
        lttw = 0
        uttw = 0
        tttw = 0
        for m in range(300):
            try:
                fn = str(m) + "team0Moves"
                fr = open(fn, "rb")
                l = pickle.load(fr)
                print(l)
                fr.close()
                lttw += len(l)
                tttw += len(l)
                lowerWins += 1
            except FileNotFoundError:
                fn = str(m) + "team1Moves"
                fr = open(fn, "rb")
                l = pickle.load(fr)
                print(l)
                fr.close()
                uttw += len(l)
                tttw += len(l)
                upperWins += 1
        print(str(lowerWins) + "," + str(upperWins) + "," + str(lttw / lowerWins) + "," + str(
            uttw / upperWins) + "," + str(tttw / 300))

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
                    r.insert(c, Pawn.Pawn("p", team, (1 * northstart) + 6 * (1 - northstart)))
                elif rn == 1 + 5 * northstart:
                    r.pop(c)
                    r.insert(c, Pawn.Pawn("p", team + 1 - 2 * team, 1 + 5 * northstart))
                if enable:
                    if rn == 0 + 7 * (1 - northstart):
                        if c == 0 or c == 7:
                            r.pop(c)
                            r.insert(c, Rook.Rook("r", team))
                        if c == 1 or c == 6:
                            r.pop(c)
                            r.insert(c, Knight.Knight("h", team))
                        if c == 2 or c == 5:
                            r.pop(c)
                            r.insert(c, Bishop.Bishop("b", team))
                        if c == 3:
                            r.pop(c)
                            r.insert(c, Queen.Queen("q", team))
                        if c == 4:
                            r.pop(c)
                            r.insert(c, King.King("k", team))
                    elif rn == 0 + 7 * northstart:
                        if c == 0 or c == 7:
                            r.pop(c)
                            r.insert(c, Rook.Rook("r", team + 1 - 2 * team))
                        if c == 1 or c == 6:
                            r.pop(c)
                            r.insert(c, Knight.Knight("h", team + 1 - 2 * team))
                        if c == 2 or c == 5:
                            r.pop(c)
                            r.insert(c, Bishop.Bishop("b", team + 1 - 2 * team))
                        if c == 3:
                            r.pop(c)
                            r.insert(c, Queen.Queen("q", team + 1 - 2 * team))
                        if c == 4:
                            r.pop(c)
                            r.insert(c, King.King("k", team + 1 - 2 * team))
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
                    print(time.perf_counter() - startTime)
                    self.displayBoard()
            print("team " + str(self.winningTeam) + " won the match!")


b = Board()
b.boardConstructor()
b.gameStart()
# b.trainingStats()
