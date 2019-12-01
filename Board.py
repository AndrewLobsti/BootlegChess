import random
import pickle
import Pawn
import Rook
import Knight
import Bishop
import Queen
import King


class Board:

    def __init__(self):
        self.board = []
        self.shadowRealm = []
        self.team0Moves = []
        self.team1Moves = []
        self.teamInCheck = 2
        self.winningTeam = 2

    def boardConstructor(self):
        self.board.clear()
        for r in range(9):
            row = []
            for c in range(9):
                if r != 0:
                    if c == 0:
                        row.append(str(r))
                    else:
                        row.append(" ")
                elif c == 0:
                    row.append("X")
                else:
                    row.append(str(c))

            self.board.append(row)

    def displayBoard(self):
        for r in self.board:
            print(r)

    def square(self, r, c):
        return self.board[r][c]

    def validIndex(self, r, c):
        return 9 > r > 0 and 9 > c > 0

    def availablePicks(self, team):
        availablePicks = []
        for r in range(1, 9):
            for c in range(1, 9):
                p = self.square(r, c)
                if not str(p).isspace():
                    if p.team == team:
                        i = [r, c]
                        availablePicks.append(i)
        return availablePicks

    def squaresInRange(self, p, cr, cc, team):
        inRange = []
        for nr in range(1, 9):
            for nc in range(1, 9):
                if p.validMove(self, cr, cc, nr, nc):
                    if self.teamInCheck != team:
                        inRange.append(self.square(nr, nc))
                    else:
                        if not self.kingInCheck(team + 1 - 2 * team):
                            inRange.append(self.square(nr, nc))
        return inRange

    def kingInCheck(self, team):
        for r in range(1, 9):
            for c in range(1, 9):
                p = self.getPiece(r, c, team)
                if str(p) != str(1):
                    s = self.squaresInRange(p, r, c, team)
                    for i in range(len(s)):
                        if str(s[i]) == " k " or str(s[i]) == " K ":
                            return True
        return False

    def inRange(self, p, cr, cc, team):
        inRange = []
        for r in range(1, 9):
            for c in range(1, 9):
                if p.validMove(self, cr, cc, r, c):
                    s = self.square(r, c)
                    self.board[r].pop(c)
                    self.board[r].insert(c, p)
                    self.board[cr][cc] = " "
                    if not self.kingInCheck(team + 1 - 2 * team):
                        self.teamInCheck = 2
                        square = [r, c]
                        inRange.append(square)
                    self.board[r].pop(c)
                    self.board[r].insert(c, s)
                    self.board[cr][cc] = p
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
        if not str(np).isspace():
            # print(str(cp) + " just ate " + str(np) + " !")
            self.shadowRealm.append(np)
            # print(self.shadowRealm)
            self.board[nr].pop(nc)
            self.board[nr].insert(nc, cp)
            self.board[cr][cc] = " "
        else:
            self.board[nr].pop(nc)
            self.board[nr].insert(nc, cp)
            self.board[cr][cc] = " "

    def promotePawn(self, r, c, team, AI):
        while True:
            p = "p"
            if AI == 0:
                p = str(input())
                p = p.lower()
            else:
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

    def drEggman(self, team):
        cM = 0
        t = team + 1 - 2 * team
        while cM == 0:
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
                    if not str(self.square(np[0], np[1])).isspace():
                        if str(self.square(np[0], np[1])) == " k " or str(self.square(np[0], np[1])) == " K ":
                            self.teamInCheck = team
                            if t == 0:
                                move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                                self.team0Moves.append(move)
                                break
                            else:
                                move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                                self.team1Moves.append(move)
                                break
                    if p.promotionRow == np[0]:
                        self.movePiece(y[0], y[1], np[0], np[1])
                        self.promotePawn(np[0], np[1], t, 1)
                        break
                    else:
                        self.movePiece(y[0], y[1], np[0], np[1])
                        break
                if not str(self.square(np[0], np[1])).isspace():
                    if str(self.square(np[0], np[1])) == " k " or str(self.square(np[0], np[1])) == " K ":
                        self.teamInCheck = team
                        if t == 0:
                            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                            self.team0Moves.append(move)
                            break
                        else:
                            move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                            self.team1Moves.append(move)
                            break
                self.movePiece(y[0], y[1], np[0], np[1])
                if t == 0:
                    move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                    self.team0Moves.append(move)
                    break
                else:
                    move = str(p) + ", " + str(y[0]) + ", " + str(y[1]) + ", " + str(np[0]) + ", " + str(np[1])
                    self.team1Moves.append(move)
                    break
            else:
                cM = 1
        if cM == 1:
            self.winningTeam = team

    def playerTurn(self, team):
        player = "Lowercase"
        if team == 1:
            player = "Uppercase"
        while True:
            print(
                player + " pieces player, choose the row and column where the piece you wish to move is located! (both values must be >= 1 and <= 8")
            r = int(input())
            c = int(input())
            if self.teamInCheck == team:
                print(
                    "You are in check! you must get your king out of harms way! If you cannot do so in 5 tries, you will automatically lose the game!")
                for t in range(6):
                    if self.validIndex(r, c):
                        k = self.getPiece(r, c, team)
                        if str(k) != str(1):
                            nr = int(input())
                            nc = int(input())
                            if nc != c or nr != r:
                                if k.validMove(self, r, c, nr, nc):
                                    self.movePiece(r, c, nr, nc)
                                    self.teamInCheck = 2
                                    if str(self.squaresInRange(k, nr, nc, t)).find("k") != -1 or str(
                                            self.squaresInRange(k, nr, nc, t)).find("K") != -1:
                                        self.teamInCheck = team + 1 - 2 * team
                                    self.displayBoard()
                                    break
                                else:
                                    print("you utter buffoon you just blew one of your tries! " + str(
                                        6 - t) + " tries remain!")
                self.winningTeam = team + 1 - 2 * team
            if self.validIndex(r, c):
                p = self.getPiece(r, c, team)
                if str(p) != str(1):
                    print("you selected the " + str(p) + " in row " + str(r) + " and column" + str(c))
                    print("if you wish to move this piece, input 1. Otherwise, input 0 to select another one. "
                          "Failure to comply with this simple instruction will not only mean you are dumb, "
                          "but will also be seen as consenting to move the selected piece")
                    w = input()
                    if int(w) + 1 != 1:
                        print("congratulations, you have just decided, or been forced to, move the "
                              "piece you previously selected! "
                              "please input the row and column where the position you want to move it to is "
                              "located.")
                        nr = int(input())
                        nc = int(input())
                        if nc != c or nr != r:
                            if p.validMove(self, r, c, nr, nc):
                                if str(p) == "p" or str(p) == "P":
                                    if p.promotionRow == nr:
                                        print(
                                            "Your pawn reached the promotion row, as such you must now promote it! type the symbol of a piece of your choice (except pawns or kings) to replace the pawn with it")
                                        self.promotePawn(nr, nc, team, 0)
                                self.movePiece(r, c, nr, nc)
                                if str(self.squaresInRange(p, nr, nc, team)).find("k") != -1 or str(
                                        self.squaresInRange(p, nr, nc, team)).find("K") != -1:
                                    self.teamInCheck = team + 1 - 2 * team
                                self.displayBoard()
                                break
                            else:
                                print(
                                    "error: that was not a position your piece could move to! please do the process all over again. Thats your reward. For being dumb.")

    def piecesOnBoard(self):
        n = 0
        for r in range(1, 9):
            for c in range(1, 9):
                if not str(self.square(r, c)).isspace():
                    n += 1
        return n

    def saveListToFile(self, t):
        if t == 0:
            l = self.team0Moves
            fn = "team0Moves"
            f = open(fn, "wb")
            pickle.dump(l, f)
            f.close()
        elif t == 1:
            l = self.team1Moves
            fn = "team1Moves"
            f = open(fn, "wb")
            pickle.dump(l, f)
            f.close()

    def spartanTrainingFacility(self):
        match = 0
        while self.winningTeam == 2:
            self.boardConstructor()
            team = random.randint(0, 1)
            northstart = random.randint(0, 1)
            for r in self.board:
                for c in range(1, 9):
                    if r[0] == str((2 * northstart) + 7 * (1 - northstart)):
                        r.pop(c)
                        r.insert(c, Pawn.Pawn("p", team, (2 * northstart) + 7 * (1 - northstart)))
                    elif r[0] == str(2 + 5 * northstart):
                        r.pop(c)
                        r.insert(c, Pawn.Pawn("p", team + 1 - 2 * team, 2 + 5 * northstart))
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
                print(r)
            turns = 0
            pr = self.piecesOnBoard()
            while turns < 500 and pr > 2 and self.winningTeam == 2:
                self.drEggman(1)
                self.drEggman(0)
                turns += 1
                pr = self.piecesOnBoard()
            match += 1
            print(match)
            self.displayBoard()
        print("team " + str(self.winningTeam) + " won the match!")
        self.displayBoard()
        if str(self.winningTeam) == str(0):
            self.saveListToFile(0)
        else:
            self.saveListToFile(1)

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
        for r in self.board:
            for c in range(1, 9):
                if r[0] == str((2 * northstart) + 7 * (1 - northstart)):
                    r.pop(c)
                    r.insert(c, Pawn.Pawn("p", team, (2 * northstart) + 7 * (1 - northstart)))
                elif r[0] == str(2 + 5 * northstart):
                    r.pop(c)
                    r.insert(c, Pawn.Pawn("p", team + 1 - 2 * team, 2 + 5 * northstart))
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
            print(r)
        while True:
            print(
                "setup complete! now select number of players: 1 for vs AI, 2 for local multiplayer and 3 for AI vs AI")
            np = int(input())
            if not 4 > np > 0:
                print("incorrect number inputed. Please input a correct number. The correct number to input is "
                      "one that is not incorrect")
            else:
                break
        if np == 2:
            print("Game Start! this is a multiplayer match, so each player takes turn moving their pieces.")
            while self.winningTeam == 2:
                self.playerTurn(0)
                self.playerTurn(1)
            print("team " + str(self.winningTeam) + " won the match!")
        elif np == 1:
            print(
                "Game Start! this is a vs AI match, so just input your move and then wait for your opponent, Dr Eggman, to input his!")
            while self.winningTeam == 2:
                if team == 0:
                    self.playerTurn(team)
                else:
                    print(
                        "Dr Eggman is the Lowercase pieces player, please wait for his eggxcelency to input his move!")
                    self.drEggman(team)
                if team == 1:
                    self.playerTurn(team)
                else:
                    print(
                        "Dr Eggman is the Uppercase pieces player, please wait for his eggxcelency to input his move!")
                    self.drEggman(team)
            print("team " + str(self.winningTeam) + " won the match!")
        elif np == 3:
            print("Game Start! this is an AI vs AI match, so just sit back and enjoy the shitshow!")
            match = 0
            while self.winningTeam == 2:
                turns = 0
                match += 1
                while turns < 500:
                    self.drEggman(1)
                    self.drEggman(0)
                    turns += 1
                print(match)
                self.displayBoard()
            print("team " + str(self.winningTeam) + " won the match!")
            if str(self.winningTeam) == 0:
                print(self.team0Moves)
            else:
                print(self.team1Moves)


b = Board()
b.boardConstructor()
b.spartanTrainingFacility()
