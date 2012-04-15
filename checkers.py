BOARD_SIZE = 8
NUM_PLAYERS = 12
PLAYERS = ["Black", "White"]

class Game:
    def __init__(self, player=0):
        self.board = Board()
        self.blackCaptured = 0
        self.whiteCaptured = 0
        # default player is black
        self.player = player
        self.turn = 0
    def run(self):
        while not (self.gameOver()):
            self.board.drawBoardState()
            print("Current Player: "+PLAYERS[self.turn])
            if (self.turn == self.player):
                # List valid moves:
                print("Valid Moves: ",end='')
                legal = self.board.calcLegalMoves(self.turn)
                print(legal)
                # get player's move
                p_row, p_col, m_row, m_col = self.getMove()
                while([(p_row,p_col),(m_row,m_col)] not in legal[0]):
                    print("Illegal move")
                    p_row, p_col, m_row, m_col = self.getMove()       
                print("Legal move")
                self.makeMove(p_row, p_col, m_row, m_col, self.turn)
            else:
                print("Computer chooses ( , )")
          #      self.board.drawBoardState()
            # switch player after move
            self.turn = 1-self.turn
    def makeMove(self, p_row, p_col, m_row, m_col, currPlayer, jump=False):
        # I'm going to need to modify this later to remove pieces on jumps
        # for now it just moves a piece
        if not jump:
            # start by making old space empty
            self.board.boardState[p_row][p_col] = -1
            # then set the new space to player who moved
            self.board.boardState[m_row][m_col] = currPlayer
            # update currPos array
            self.board.currPos[currPlayer].remove((p_row, p_col))
            self.board.currPos[currPlayer].append((m_row, m_col))

    # need to modify this to deal with jumps    
    def getMove(self):
        print("Pick a piece to move")
        p_row = int(input("Row: "))
        p_col = int(input("Col: "))
        print("Pick a cell to move to")
        m_row = int(input("Row: "))
        m_col = int(input("Col: "))
        return p_row, p_col, m_row, m_col
    def gameOver(self):
        if (NUM_PLAYERS == self.blackCaptured or NUM_PLAYERS == self.whiteCaptured):
            return True
        else:
            return False
        
class Board:
    def __init__(self, board=[], currBlack=[], currWhite=[]):
        if (board!=[]):
            self.boardState = board     
        else:
            self.setDefaultBoard()
        self.__currPos = [[],[]]
        if (currBlack != []):
            self.currPos[0] = currBlack
        else:
            self.currPos[0] = self.calcPos(0)
        if (currWhite != []):
            self.currPos[1] = currWhite
        else:
            self.currPos[1] = self.calcPos(1)            
    def boardMove(self, move, currPlayer, jump=False):
            # start by making old space empty
            self.boardState[move[0][0]][move[0][1]] = -1
            if not jump:
                # then set the new space to player who moved
                self.board.boardState[move[1][0]][move[1][1]] = currPlayer
            else:
                #do stuff for jump here
            # update currPos array
            # if its jump, the board could be in many configs, just recalc it
            if jump:
                self.currPos[0] = self.calcPos(0)
                self.currPos[1] = self.calcPos(1)
            # otherwise change is predictable, so faster to just set it
            else:
                self.__currPos[currPlayer].remove((move[0][0], move[0][1]))
                self.__currPos[currPlayer].append((move[1][0], move[1][1]))

    def calcLegalMoves(self, player): # int array  -> [0] reg, [1] jump
        legalMoves = [[],[]]
        # next goes up if black or down if white
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else 7
#        print(self.currPos[player])
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                break
            # calc regular moves first
            # diagonal right, only search if not at right edge of board
            if (cell[1]!=BOARD_SIZE-1 and self.boardState[cell[0]+next][cell[1]+1]==-1):
                legalMoves[0].append([(cell[0],cell[1]),(cell[0]+next,cell[1]+1)])
            # diagonal left, only search if not at left edge of board
            if (cell[1]!=0 and self.boardState[cell[0]+next][cell[1]-1]==-1):
                legalMoves[0].append([(cell[0],cell[1]),(cell[0]+next,cell[1]-1)])
        return legalMoves
    def calcPos(self, player):
        pos = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.boardState[row][col]==player):
                    pos.append((row,col))
        return pos
    
     
    def drawBoardState(self):
        for colnum in range(BOARD_SIZE):
            print(str(colnum)+" ",end="")
        print("")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (self.boardState[row][col] == -1):
                    print("+ ",end='')
                elif (self.boardState[row][col] == 1):
                    print("W ",end='')
                elif (self.boardState[row][col] == 0):
                    print("B ",end='')
            print(str(row))

    def setDefaultBoard(self):
        # reset board
        # -1 = empty, 0=black, 1=white
        self.boardState = [
            [-1,1,-1,1,-1,1,-1,1],
            [1,-1,1,-1,1,-1,1,-1],
            [-1,1,-1,1,-1,1,-1,1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1]
        ]


def main():
    test = Game()
    test.run()
  #  test.drawBoardState()
main()
