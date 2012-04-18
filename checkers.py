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
                self.makeMove(move) 
            else:
                legal = self.board.calcLegalMoves(self.turn)
                choice = random.randint(0,len(legal)-1)
                self.makeMove(legal[choice])
                print("Computer chooses ("+str(legal[choice].start)+", "+str(legal[choice].end)+")")
            # switch player after move
            self.turn = 1-self.turn
    def makeMove(self, move):
        # I'm going to need to modify this later to remove pieces on jumps
        # for now it just moves a piece

        self.board.boardMove(move, self.turn)        
  
    def getMove(self):
        legal = self.board.calcLegalMoves(self.turn)
        move = -1
        while move not in range(len(legal)):
            # List valid moves:
            print("Valid Moves: ")
            for i in range(len(legal)):
                print(str(i+1)+": ",end='')
                print(str(legal[i].start)+" "+str(legal[i].end))
            move = int(input("Pick a move: "))-1
            if move not in range(len(legal)):
                print("Illegal move")
        print("Legal move")
        return (legal[move])         
    def gameOver(self):
        if (NUM_PLAYERS == self.captured[0] or NUM_PLAYERS == self.captured[1]):
            return True
        else:
            return False

class Move:
    def __init__(self, start, end, jump=False):
            self.start = start
            self.end = end # tuple (row, col)
            self.jump = jump # bool
            self.jumpOver = [] # array of pieces jumped over
#            self.player = player
        
    
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
    def boardMove(self, move_info, currPlayer):
        move = [move_info.start, move_info.end]
        remove = move_info.jumpOver
        jump = move_info.jump
        # start by making old space empty
        self.boardState[move[0][0]][move[0][1]] = -1
        # then set the new space to player who moved
        self.boardState[move[1][0]][move[1][1]] = currPlayer
        if jump:
            #remove jumped over enemies
            for enemy in move_info.jumpOver:
                self.boardState[enemy[0]][enemy[1]] = -1
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
        legalMoves = []
        hasJumps = False
        # next goes up if black or down if white
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else 7
        # cell refers to a position tuple (row, col)
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                break
            # diagonal right, only search if not at right edge of board
            if (cell[1]!=BOARD_SIZE-1):
                #empty, regular move
                if (self.boardState[cell[0]+next][cell[1]+1]==-1 and not hasJumps):
                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]+1)) 
                    legalMoves.append(temp)
                # has enemy, can jump it?
                elif(self.boardState[cell[0]+next][cell[1]+1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), False, player)
                    if (len(jumps)!=0):
                        # if first jump, clear out regular moves
                        if not hasJumps:
                            hasJumps = True
                            legalMoves = []
                        legalMoves.extend(jumps)
                        print(legalMoves)
            # diagonal left, only search if not at left edge of board
            if (cell[1]!=0):
                if(self.boardState[cell[0]+next][cell[1]-1]==-1 and not hasJumps):
                    temp = Move((cell[0],cell[1]),(cell[0]+next,cell[1]-1)) 
                    legalMoves.append(temp)                    
                elif(self.boardState[cell[0]+next][cell[1]-1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), True, player)
                    if (len(jumps)!=0):
                        if not hasJumps:
                            hasJumps = True
                            legalMoves = []                        
                        legalMoves.extend(jumps)
                        
        return legalMoves

    def NewcalcLegalMoves(self, player):
        legalMoves = [] 
        # next goes up if black or down if white
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else 7
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                break
            # diagonal right, only search if not at right edge of board
            if (cell[1]!=BOARD_SIZE-1):
                if (self.boardState[cell[0]+next][cell[1]+1]==-1):
                    legalMoves[0].append([[(cell[0],cell[1]),(cell[0]+next,cell[1]+1)]])
                elif(self.boardState[cell[0]+next][cell[1]+1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), False, player)
                    if (len(jumps)!=0):
                        print(legalMoves[1])
            # diagonal left, only search if not at left edge of board
            if (cell[1]!=0):
                if(self.boardState[cell[0]+next][cell[1]-1]==-1):
                    legalMoves[0].append([[(cell[0],cell[1]),(cell[0]+next,cell[1]-1)]])
                elif(self.boardState[cell[0]+next][cell[1]-1]==1-player):
                    jumps = self.checkJump((cell[0],cell[1]), True, player)
                    if (len(jumps)!=0):
                        legalMoves[1].extend(jumps)
        return legalMoves

    # enemy is the square we plan to jump over
    # change later to deal with double jumps
    def checkJump(self, cell, isLeft, player):
        jumps = []
        next = -1 if player == 0 else 1                
        #check top left
        if (isLeft):
            if (cell[1]>1 and self.boardState[cell[0]+next+next][cell[1]-2]==-1):
                temp = Move(cell, (cell[0]+next+next, cell[1]-2), True)
                temp.jumpOver = [(cell[0]+next,cell[1]-1)]
                jumps.append(temp)
        else:
        #check top right
            if (cell[1]<BOARD_SIZE-2 and self.boardState[cell[0]+next+next][cell[1]+2]==-1):
                # ([original cell, new cell], enemy cell])
                temp = Move(cell, (cell[0]+next+next, cell[1]+2), True)
                temp.jumpOver = [(cell[0]+next,cell[1]+1)]
                jumps.append(temp)                
        print("Jumps:")
        for mov in jumps:
            print(str(mov.start)+" "+str(mov.end)+" Jump over: "+str(mov.jumpOver))
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
