from .termcolor import colored


WHITE = True
BLACK = False
X = 0
Y = 1

class Coordinate(tuple):

    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __reduce__(self):
        return (self.__class__, tuple(self))

    def __add__(self, other):
        return Coordinate(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Coordinate(self[0] - other[0], self[1] - other[1])


class Move:

    def __init__(self, piece, newPos, pieceToCapture=None):
        self.notation = None
        self.check = False
        self.checkmate = False
        self.kingsideCastle = False
        self.queensideCastle = False
        self.promotion = False
        self.passant = False
        self.stalemate = False

        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.pieceToCapture = pieceToCapture
        # For en passant and castling
        self.specialMovePiece = None
        # For castling
        self.rookMove = None

    def __str__(self):
        displayString = 'Old pos : ' + str(self.oldPos) + \
                        ' -- New pos : ' + str(self.newPos)
        if self.notation:
            displayString += ' Notation : ' + self.notation
        if self.passant:
            displayString = 'Old pos : ' + str(self.oldPos) + \
                            ' -- New pos : ' + str(self.newPos) + \
                            ' -- Pawn taken : ' + str(self.specialMovePiece)
            displayString += ' PASSANT'
        return displayString

    def __eq__(self, other):
        if self.oldPos == other.oldPos and \
           self.newPos == other.newPos and \
           self.specialMovePiece == other.specialMovePiece:
            if not self.specialMovePiece:
                return True
            if self.specialMovePiece and \
               self.specialMovePiece == other.specialMovePiece:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash((self.oldPos, self.newPos))

    def reverse(self):
        return Move(self.piece, self.piece.position,
                    pieceToCapture=self.pieceToCapture)


class Piece:

    def __init__(self, board, side, position, movesMade=0):
        self.board = board
        self.side = side
        self.position = position
        self.movesMade = 0

    def __str__(self):
        sideString = 'White' if self.side == WHITE else 'Black'
        return 'Type : ' + type(self).__name__ + \
               ' - Position : ' + str(self.position) + \
               " - Side : " + sideString + \
               ' -- Value : ' + str(self.value) + \
               " -- Moves made : " + str(self.movesMade)

    def movesInDirectionFromPos(self, pos, direction, side):
        for dis in range(1, 8):
            movement = Coordinate(dis * direction[X], dis * direction[Y])
            newPos = pos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)

                elif pieceAtNewPos is not None:
                    if pieceAtNewPos.side != side:
                        yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
                    return

    def __eq__(self, other):
        if self.board == other.board and \
           self.side == other.side and \
           self.position == other.position and \
           self.__class__ == other.__class__:
            return True
        return False

    def copy(self):
        cpy = self.__class__(self.board, self.side, self.position,
                             movesMade=self.movesMade)
        return cpy


class King (Piece):

    stringRep = 'K'
    value = 100

    def __init__(self, board, side, position,  movesMade=0):
        super(King, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPos = self.position
        movements = [Coordinate(0, 1), Coordinate(0, -1), Coordinate(1, 0), Coordinate(-1, 0), Coordinate(1, 1),
                     Coordinate(1, -1), Coordinate(-1, 1), Coordinate(-1, -1)]
        for movement in movements:
            newPos = currentPos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if self.board.pieceAtPosition(newPos) is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)

        # Castling
        if self.movesMade == 0:
            inCheck = False
            kingsideCastleBlocked = False
            queensideCastleBlocked = False
            kingsideCastleCheck = False
            queensideCastleCheck = False
            kingsideRookMoved = True
            queensideRookMoved = True

            kingsideCastlePositions = [self.position + Coordinate(1, 0),
                                       self.position + Coordinate(2, 0)]
            for pos in kingsideCastlePositions:
                if self.board.pieceAtPosition(pos):
                    kingsideCastleBlocked = True
                    break

            queensideCastlePositions = [self.position - Coordinate(1, 0),
                                        self.position - Coordinate(2, 0),
                                        self.position - Coordinate(3, 0)]
            for pos in queensideCastlePositions:
                if self.board.pieceAtPosition(pos):
                    queensideCastleBlocked = True
                    break

            if kingsideCastleBlocked and queensideCastleBlocked:
                return

            otherSideMoves = \
                self.board.getAllMovesUnfiltered(not self.side,
                                                 includeKing=False)
            for move in otherSideMoves:
                if move.newPos == self.position:
                    inCheck = True
                    break
                if move.newPos == self.position + Coordinate(1, 0) or \
                   move.newPos == self.position + Coordinate(2, 0):
                    kingsideCastleCheck = True
                if move.newPos == self.position - Coordinate(1, 0) or \
                   move.newPos == self.position - Coordinate(2, 0):
                    queensideCastleCheck = True

            kingsideRookPos = self.position + Coordinate(3, 0)
            kingsideRook = self.board.pieceAtPosition(kingsideRookPos) \
                if self.board.isValidPos(kingsideRookPos) \
                else None
            if kingsideRook and \
               kingsideRook.stringRep == 'R' and \
               kingsideRook.movesMade == 0:
                kingsideRookMoved = False

            queensideRookPos = self.position - Coordinate(4, 0)
            queensideRook = self.board.pieceAtPosition(queensideRookPos) \
                if self.board.isValidPos(queensideRookPos) \
                else None
            if queensideRook and \
               queensideRook.stringRep == 'R' and \
               queensideRook.movesMade == 0:
                queensideRookMoved = False

            if not inCheck:
                if not kingsideCastleBlocked and \
                   not kingsideCastleCheck and \
                   not kingsideRookMoved:
                    move = Move(self, self.position + Coordinate(2, 0))
                    rookMove = Move(kingsideRook, self.position + Coordinate(1, 0))
                    move.specialMovePiece = \
                        self.board.pieceAtPosition(kingsideRookPos)
                    move.kingsideCastle = True
                    move.rookMove = rookMove
                    yield move
                if not queensideCastleBlocked and \
                   not queensideCastleCheck and \
                   not queensideRookMoved:
                    move = Move(self, self.position - Coordinate(2, 0))
                    rookMove = Move(queensideRook, self.position - Coordinate(1, 0))
                    move.specialMovePiece = \
                        self.board.pieceAtPosition(queensideRookPos)
                    move.queensideCastle = True
                    move.rookMove = rookMove
                    yield move


class Queen(Piece):

    stringRep = 'Q'
    value = 9

    def __init__(self, board, side, position, movesMade=0):
        super(Queen, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position

        directions = [Coordinate(0, 1), Coordinate(0, -1), Coordinate(1, 0), Coordinate(-1, 0), Coordinate(1, 1),
                      Coordinate(1, -1), Coordinate(-1, 1), Coordinate(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,
                                                     direction, self.side):
                yield move


class Rook(Piece):

    stringRep = 'R'
    value = 5

    def __init__(self, board, side, position,  movesMade=0):
        super(Rook, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position

        directions = [Coordinate(0, 1), Coordinate(0, -1), Coordinate(1, 0), Coordinate(-1, 0)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,
                                                     direction, self.side):
                yield move


class Bishop (Piece):

    stringRep = 'B'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        super(Bishop, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        currentPosition = self.position
        directions = [Coordinate(1, 1), Coordinate(1, -1), Coordinate(-1, 1), Coordinate(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,
                                                     direction, self.side):
                yield move


class Knight(Piece):

    stringRep = 'N'
    value = 3

    def __init__(self, board, side, position,  movesMade=0):
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        currentPos = self.position
        movements = [Coordinate(2, 1), Coordinate(2, -1), Coordinate(-2, 1), Coordinate(-2, -1), Coordinate(1, 2),
                     Coordinate(1, -2), Coordinate(-1, -2), Coordinate(-1, 2)]
        for movement in movements:
            newPos = currentPos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)


class Pawn(Piece):

    stringRep = 'P'
    value = 1

    def __init__(self, board, side, position,  movesMade=0):
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

    # @profile
    def getPossibleMoves(self):
        currentPosition = self.position

        # Pawn moves one up
        movement = Coordinate(0, 1) if self.side == WHITE else Coordinate(0, -1)
        advanceOnePosition = currentPosition + movement
        if self.board.isValidPos(advanceOnePosition):
            # Promotion moves
            if self.board.pieceAtPosition(advanceOnePosition) is None:
                col = advanceOnePosition[1]
                if col == 7 or col == 0:
                    piecesForPromotion = \
                        [Rook(self.board, self.side, advanceOnePosition),
                         Knight(self.board, self.side, advanceOnePosition),
                         Bishop(self.board, self.side, advanceOnePosition),
                         Queen(self.board, self.side, advanceOnePosition)]
                    for piece in piecesForPromotion:
                        move = Move(self, advanceOnePosition)
                        move.promotion = True
                        move.specialMovePiece = piece
                        yield move
                else:
                    yield Move(self, advanceOnePosition)

        # Pawn moves two up
        if self.movesMade == 0:
            movement = Coordinate(0, 2) if self.side == WHITE else Coordinate(0, -2)
            advanceTwoPosition = currentPosition + movement
            if self.board.isValidPos(advanceTwoPosition):
                if self.board.pieceAtPosition(advanceTwoPosition) is None and \
                   self.board.pieceAtPosition(advanceOnePosition) is None:
                    yield Move(self, advanceTwoPosition)

        # Pawn takes
        movements = [Coordinate(1, 1), Coordinate(-1, 1)] \
            if self.side == WHITE else [Coordinate(1, -1), Coordinate(-1, -1)]

        for movement in movements:
            newPosition = self.position + movement
            if self.board.isValidPos(newPosition):
                pieceToTake = self.board.pieceAtPosition(newPosition)
                if pieceToTake and pieceToTake.side != self.side:
                    col = newPosition[1]
                    # Promotions
                    if col == 7 or col == 0:
                        piecesForPromotion = \
                            [Rook(self.board, self.side, newPosition),
                             Knight(self.board, self.side, newPosition),
                             Bishop(self.board, self.side, newPosition),
                             Queen(self.board, self.side, newPosition)]
                        for piece in piecesForPromotion:
                            move = Move(self, newPosition, pieceToCapture=pieceToTake)
                            move.promotion = True
                            move.specialMovePiece = piece
                            yield move
                    else:
                        yield Move(self, newPosition,
                                   pieceToCapture=pieceToTake)

        # En passant
        movements = [Coordinate(1, 1), Coordinate(-1, 1)] \
            if self.side == WHITE else [Coordinate(1, -1), Coordinate(-1, -1)]
        for movement in movements:
            posBesidePawn = self.position + Coordinate(movement[0], 0)
            if self.board.isValidPos(posBesidePawn):
                pieceBesidePawn = self.board.pieceAtPosition(posBesidePawn)
                lastPieceMoved = self.board.getLastPieceMoved()
                lastMoveWasAdvanceTwo = False
                lastMove = self.board.getLastMove()

                if lastMove:
                    if lastMove.newPos - lastMove.oldPos == Coordinate(0, 2) or \
                       lastMove.newPos - lastMove.oldPos == Coordinate(0, -2):
                        lastMoveWasAdvanceTwo = True

                if pieceBesidePawn and \
                   pieceBesidePawn.stringRep == 'P' and \
                   pieceBesidePawn.side != self.side and \
                   lastPieceMoved is pieceBesidePawn and \
                   lastMoveWasAdvanceTwo:
                    move = Move(self, self.position + movement,
                                pieceToCapture=pieceBesidePawn)
                    move.passant = True
                    move.specialMovePiece = pieceBesidePawn
                    yield move


class Board:

    def __init__(self, mateInOne=False, castleBoard=False,
                 passant=False, promotion=False):
        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0
        self.checkmate = False

        if not mateInOne and not castleBoard and not passant and not promotion:
            self.pieces.extend([Rook(self, BLACK, Coordinate(0, 7)),
                                Knight(self, BLACK, Coordinate(1, 7)),
                                Bishop(self, BLACK, Coordinate(2, 7)),
                                Queen(self, BLACK, Coordinate(3, 7)),
                                King(self, BLACK, Coordinate(4, 7)),
                                Bishop(self, BLACK, Coordinate(5, 7)),
                                Knight(self, BLACK, Coordinate(6, 7)),
                                Rook(self, BLACK, Coordinate(7, 7))])
            for x in range(8):
                self.pieces.append(Pawn(self, BLACK, Coordinate(x, 6)))
            for x in range(8):
                self.pieces.append(Pawn(self, WHITE, Coordinate(x, 1)))
            self.pieces.extend([Rook(self, WHITE, Coordinate(0, 0)),
                                Knight(self, WHITE, Coordinate(1, 0)),
                                Bishop(self, WHITE, Coordinate(2, 0)),
                                Queen(self, WHITE, Coordinate(3, 0)),
                                King(self, WHITE, Coordinate(4, 0)),
                                Bishop(self, WHITE, Coordinate(5, 0)),
                                Knight(self, WHITE, Coordinate(6, 0)),
                                Rook(self, WHITE, Coordinate(7, 0))])

        elif promotion:
            pawnToPromote = Pawn(self, WHITE, Coordinate(1, 6))
            pawnToPromote.movesMade = 1
            kingWhite = King(self, WHITE, Coordinate(4, 0))
            kingBlack = King(self, BLACK, Coordinate(3, 2))
            self.pieces.extend([pawnToPromote, kingWhite, kingBlack])

        elif passant:
            pawn = Pawn(self, WHITE, Coordinate(1, 4))
            pawn2 = Pawn(self, BLACK, Coordinate(2, 6))
            kingWhite = King(self, WHITE, Coordinate(4, 0))
            kingBlack = King(self, BLACK, Coordinate(3, 2))
            self.pieces.extend([pawn, pawn2, kingWhite, kingBlack])
            self.history = []
            self.currentSide = BLACK
            self.points = 0
            self.movesMade = 0
            self.checkmate = False
            firstMove = Move(pawn2, Coordinate(2, 4))
            self.makeMove(firstMove)
            self.currentSide = WHITE
            return

    def __str__(self):
        return self.wrapStringRep(self.makeStringRep(self.pieces))

    def undoLastMove(self):
        lastMove, pieceTaken = self.history.pop()

        if lastMove.queensideCastle or lastMove.kingsideCastle:
            king = lastMove.piece
            rook = lastMove.specialMovePiece

            self.movePieceToPosition(king, lastMove.oldPos)
            self.movePieceToPosition(rook, lastMove.rookMove.oldPos)

            king.movesMade -= 1
            rook.movesMade -= 1

        elif lastMove.passant:
            pawnMoved = lastMove.piece
            pawnTaken = pieceTaken
            self.pieces.append(pawnTaken)
            self.movePieceToPosition(pawnMoved, lastMove.oldPos)
            pawnMoved.movesMade -= 1
            if pawnTaken.side == WHITE:
                self.points += 1
            if pawnTaken.side == BLACK:
                self.points -= 1

        elif lastMove.promotion:
            pawnPromoted = lastMove.piece
            promotedPiece = self.pieceAtPosition(lastMove.newPos)
            self.pieces.remove(promotedPiece)
            if pieceTaken:
                if pieceTaken.side == WHITE:
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK:
                    self.points -= pieceTaken.value
                self.pieces.append(pieceTaken)
            self.pieces.append(pawnPromoted)
            if pawnPromoted.side == WHITE:
                self.points -= promotedPiece.value - 1
            elif pawnPromoted.side == BLACK:
                self.points += promotedPiece.value - 1
            pawnPromoted.movesMade -= 1

        else:
            pieceToMoveBack = lastMove.piece
            self.movePieceToPosition(pieceToMoveBack, lastMove.oldPos)
            if pieceTaken:
                if pieceTaken.side == WHITE:
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK:
                    self.points -= pieceTaken.value
                self.addPieceToPosition(pieceTaken, lastMove.newPos)
                self.pieces.append(pieceTaken)
            pieceToMoveBack.movesMade -= 1

        self.currentSide = not self.currentSide

    def isCheckmate(self):
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == "K":
                    return True
        return False

    def isStalemate(self):
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == "K":
                    return False
            return True
        return False

    def getLastMove(self):
        if self.history:
            return self.history[-1][0]

    def getLastPieceMoved(self):
        if self.history:
            return self.history[-1][0].piece

    def addMoveToHistory(self, move):
        pieceTaken = None
        if move.passant:
            pieceTaken = move.specialMovePiece
            self.history.append([move, pieceTaken])
            return
        pieceTaken = move.pieceToCapture
        if pieceTaken:
            self.history.append([move, pieceTaken])
            return

        self.history.append([move, None])

    def getCurrentSide(self):
        return self.currentSide
    
    def makeStringRep(self, pieces):
        stringRep = ''
        for y in range(7, -1, -1):
            for x in range(8):
                piece = None
                for p in pieces:
                    if p.position == Coordinate(x, y):
                        piece = p
                        break
                pieceRep = ''
                if piece:
                    side = piece.side
                    color = 'blue' if side == WHITE else 'red'
                    pieceRep = colored(piece.stringRep, color)
                else:
                    pieceRep = ' '
                stringRep += pieceRep + ' '
            stringRep += '\n'
        return stringRep.rstrip()
    
    def makeUnicodeStringRep(self, pieces):
        DISPLAY_LOOKUP = {
            "R": '♜',
            "N": '♞',
            "B": '♝',
            "K": '♚',	
            "Q": '♛',
            "P": '♟',
        }

        stringRep = ''
        for y in range(7, -1, -1):
            for x in range(8):
                piece = None
                for p in pieces:
                    if p.position == Coordinate(x, y):
                        piece = p
                        break
                on_color = 'on_cyan' if y % 2 == x % 2 else 'on_yellow'
                pieceRep = colored('  ', on_color=on_color)
                if piece:
                    side = piece.side
                    color = 'white' if side == WHITE else 'grey'
                    pieceRep = colored(piece.stringRep + ' ', color=color, on_color=on_color)
                stringRep += pieceRep
            stringRep += '\n'
        return stringRep.rstrip()

    def wrapStringRep(self, stringRep):
        sRep = '\n'.join(
            ['%d  %s' % (8-r, s.rstrip())
             for r, s in enumerate(stringRep.split('\n'))] +
            [' '*21, '   a b c d e f g h']
            ).rstrip()
        return sRep

    def rankOfPiece(self, piece):
        return str(piece.position[1] + 1)

    def fileOfPiece(self, piece):
        transTable = str.maketrans('01234567', 'abcdefgh')
        return str(piece.position[0]).translate(transTable)

    def getCoordinateNotationOfMove(self, move):
        notation = ""
        notation += self.positionToHumanCoord(move.oldPos)
        notation += self.positionToHumanCoord(move.newPos)

        if move.promotion:
            notation += str(move.specialMovePiece.stringRep)

        return notation

    def getCaptureNotation(self, move, short=False):
        notation = ""
        pieceToMove = move.piece
        pieceToTake = move.pieceToCapture

        if type(pieceToMove) is Pawn:
            notation += self.fileOfPiece(pieceToMove)
        else:
            notation += pieceToMove.stringRep
        notation += 'x'
        if short:
            notation += pieceToTake.stringRep
        else:
            notation += self.positionToHumanCoord(move.newPos)

        if move.promotion:
            notation += str(move.specialMovePiece.stringRep)

        return notation

    def currentSideRep(self):
        return "White" if self.currentSide else "Black"

    def getAlgebraicNotationOfMove(self, move, short=True):
        notation = ""
        pieceToMove = move.piece
        pieceToTake = move.pieceToCapture

        if move.queensideCastle:
            return "O-O-O"

        if move.kingsideCastle:
            return "O-O"

        if not short or type(pieceToMove) is not Pawn:
            notation += pieceToMove.stringRep

        if pieceToTake is not None:
            if short and type(pieceToMove) is Pawn:
                notation += self.fileOfPiece(pieceToMove)
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)

        if move.promotion:
            notation += "=" + str(move.specialMovePiece.stringRep)

        return notation

    def getAlgebraicNotationOfMoveWithFile(self, move, short=True):
        # TODO: Use self.getAlgebraicNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if not short or type(pieceToMove) is not Pawn:
            notation += pieceToMove.stringRep
        notation += self.fileOfPiece(pieceToMove)

        if pieceToTake is not None:
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    def getAlgebraicNotationOfMoveWithRank(self, move, short=True):
        # TODO: Use self.getAlgebraicNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if not short or type(pieceToMove) is not Pawn:
            notation += pieceToMove.stringRep

        notation += self.rankOfPiece(pieceToMove)

        if pieceToTake is not None:
            if short and type(pieceToMove) is Pawn:
                notation += self.fileOfPiece(pieceToMove)
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    def getAlgebraicNotationOfMoveWithFileAndRank(self, move, short=True):
        # TODO: Use self.getAlgebraicNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if not short or type(pieceToMove) is not Pawn:
            notation += pieceToMove.stringRep

        notation += self.fileOfPiece(pieceToMove)
        notation += self.rankOfPiece(pieceToMove)

        if pieceToTake is not None:
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    def humanCoordToPosition(self, coord):
        transTable = str.maketrans('abcdefgh', '12345678')
        coord = coord.translate(transTable)
        coord = [int(c)-1 for c in coord]
        pos = Coordinate(coord[0], coord[1])
        return pos

    def positionToHumanCoord(self, pos):
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1]+1)
        return notation

    def isValidPos(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def getSideOfMove(self, move):
        return move.piece.side

    def getPositionOfPiece(self, piece):
        for y in range(8):
            for x in range(8):
                if self.boardArray[y][x] is piece:
                    return Coordinate(x, 7-y)

    def pieceAtPosition(self, pos):
        for piece in self.pieces:
            if piece.position == pos:
                return piece

    def movePieceToPosition(self, piece, pos):
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        piece.position = pos

    def clearPosition(self, pos):
        x, y = self.coordToLocationInArray(pos)
        self.boardArray[x][y] = None

    def coordToLocationInArray(self, pos):
        return (7-pos[1], pos[0])

    def locationInArrayToCoord(self, loc):
        return (loc[1], 7-loc[0])

    def makeMove(self, move):
        self.addMoveToHistory(move)
        if move.kingsideCastle or move.queensideCastle:
            kingToMove = move.piece
            rookToMove = move.specialMovePiece
            self.movePieceToPosition(kingToMove, move.newPos)
            self.movePieceToPosition(rookToMove, move.rookMove.newPos)
            kingToMove.movesMade += 1
            rookToMove.movesMade += 1

        elif move.passant:
            pawnToMove = move.piece
            pawnToTake = move.specialMovePiece
            pawnToMove.position = move.newPos
            self.pieces.remove(pawnToTake)
            pawnToMove.movesMade += 1

        elif move.promotion:
            pieceToTake = move.pieceToCapture
            self.pieces.remove(move.piece)
            if pieceToTake:
                if pieceToTake.side == WHITE:
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK:
                    self.points += pieceToTake.value
                self.pieces.remove(pieceToTake)

            self.pieces.append(move.specialMovePiece)
            if move.piece.side == WHITE:
                self.points += move.specialMovePiece.value - 1
            if move.piece.side == BLACK:
                self.points -= move.specialMovePiece.value - 1
            move.piece.movesMade += 1

        else:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture

            if pieceToTake:
                if pieceToTake.side == WHITE:
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK:
                    self.points += pieceToTake.value
                self.pieces.remove(pieceToTake)

            self.movePieceToPosition(pieceToMove, move.newPos)
            pieceToMove.movesMade += 1
        self.movesMade += 1
        self.currentSide = not self.currentSide

    def getPointValueOfSide(self, side):
        points = 0
        for piece in self.pieces:
            if piece.side == side:
                points += piece.value
        return points

    def getPointAdvantageOfSide(self, side):
        pointAdvantage = self.getPointValueOfSide(side) - \
            self.getPointValueOfSide(not side)
        return pointAdvantage
        if side == WHITE:
            return self.points
        if side == BLACK:
            return -self.points

    def getAllMovesUnfiltered(self, side, includeKing=True):
        unfilteredMoves = []
        for piece in self.pieces:
            if piece.side == side:
                if includeKing or piece.stringRep != 'K':
                    for move in piece.getPossibleMoves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        for move in self.getAllMovesUnfiltered(side):
            pieceToTake = move.pieceToCapture
            if pieceToTake and pieceToTake.stringRep == 'K':
                return False
        return True

    def moveIsLegal(self, move):
        side = move.piece.side
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal

    # TODO: remove side parameter, unneccesary
    def getAllMovesLegal(self, side):
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
