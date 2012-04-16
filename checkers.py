import random

BOARD_SIZE = 8
NUM_PLAYERS = 12
PLAYERS = ["Black", "White"]

class Game:
    def __init__(self, player=0):
        self.board = Board()
        self.captured = [0,0]
        # default player is black
        self.player = player
        self.turn = 0
    def run(self):
        while not (self.gameOver()):
            self.board.drawBoardState()
            print("Current Player: "+PLAYERS[self.turn])
            if (self.turn == self.player):
                # get player's move
                move = self.getMove()
                self.makeMove(move, self.turn) 
            else:
                legal = self.board.calcLegalMoves(self.turn)
                choice = random.randint(0,len(legal[0])-1)
                self.makeMove(legal[0][choice], self.turn)
                print("Computer chooses ("+str(legal[0][choice][0])+", "+str(legal[0][choice][1])+")")
            # switch player after move
            self.turn = 1-self.turn
    def makeMove(self, move, currPlayer, jump=False):
        # I'm going to need to modify this later to remove pieces on jumps
        # for now it just moves a piece
        if not jump:
            self.board.boardMove(move, currPlayer)
        
            # do stuff for jump
    # need to modify this to deal with jumps    
    def getMove(self):
        legal = self.board.calcLegalMoves(self.turn)
        move = -1
        while move not in range(len(legal[0])):
            # List valid moves:
            print("Valid Moves: ")
            for i in range(len(legal[0])):
                print(str(i+1)+": ",end='')
                print(legal[0][i])
            move = int(input("Pick a move: "))-1
            if move not in range(len(legal[0])):
                print("Illegal move")
        print("Legal move")
        return legal[0][move]            
    def gameOver(self):
        if (NUM_PLAYERS == self.captured[0] or NUM_PLAYERS == self.captured[1]):
            return True
        else:
            return False
        
class Board:
    def __init__(self, board=[], currBlack=[], currWhite=[]):
        if (board!=[]):
            self.boardState = board     
        else:
            self.setDefaultBoard()
        self.currPos = [[],[]]
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
            self.boardState[move[1][0]][move[1][1]] = currPlayer
            #do stuff for jump here
        # update currPos array
        # if its jump, the board could be in many configs, just recalc it
        if jump:
            self.currPos[0] = self.calcPos(0)
            self.currPos[1] = self.calcPos(1)
        # otherwise change is predictable, so faster to just set it
        else:
            self.currPos[currPlayer].remove((move[0][0], move[0][1]))
            self.currPos[currPlayer].append((move[1][0], move[1][1]))

    def calcLegalMoves(self, player): # int array  -> [0] reg, [1] jump
        legalMoves = [[],[]]
        # next goes up if black or down if white
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else 7
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                break
            # diagonal right, only search if not at right edge of board
            if (cell[1]!=BOARD_SIZE-1):
                if (self.boardState[cell[0]+next][cell[1]+1]==-1):
                    legalMoves[0].append([(cell[0],cell[1]),(cell[0]+next,cell[1]+1)])
                elif(self.boardState[cell[0]+next][cell[1]+1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), True, player)
                    if (len(jumps)!=0):
                        legalMoves[1].append(jumps)
            # diagonal left, only search if not at left edge of board
            if (cell[1]!=0):
                if(self.boardState[cell[0]+next][cell[1]-1]==-1):
                    legalMoves[0].append([(cell[0],cell[1]),(cell[0]+next,cell[1]-1)])
                elif(self.boardState[cell[0]+next][cell[1]-1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), False, player)
                    if (len(jumps)!=0):
                        legalMoves[1].append(jumps)
        return legalMoves

    # enemy is the square we plan to jump over
    # change later to deal with double jumps
    def checkJump(self, cell, isLeft, player):
        jumps = []
        next = -1 if player == 0 else 1                
        #check top left
        if (isLeft):
            if (cell[1]>1 and self.boardState[cell[0]+next+next][cell[1]-2]==-1):
                jumps.append([cell, (cell[0]+next+next, cell[1]-2)])
        else:
        #check top right
            if (cell[1]<BOARD_SIZE-2 and self.boardState[cell[0]+next+next][cell[1]+2]==-1):
                jumps.append([cell, (cell[0]+next+next, cell[1]+2)])
        print("Jumps:")
        print(jumps)
        return jumps
    
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
