# Next steps:
# X 1. Implement game-over evaluation func
# 2. Alpha-beta search
# 3. Starting screen - choose player
# 4. Double jumps
# 5. Difficulty levels (depth-limit)

import random

BOARD_SIZE = 8
NUM_PLAYERS = 12
# the players array extends to many other arrays in the program
# in these arrays, 0 will refer to black and 1 to white
PLAYERS = ["Black", "White"]

class Game:
    def __init__(self, player=0):
        self.board = Board()
        # refers to how many pieces that play
        self.remaining = [NUM_PLAYERS, NUM_PLAYERS]
        # default player is black
        self.player = player
        self.turn = 0
    def run(self):
        while not (self.gameOver()):
            self.board.drawBoardState()
            print("Current Player: "+PLAYERS[self.turn])
            if (self.turn == self.player):
                # get player's move
                legal = self.board.calcLegalMoves(self.turn)
                if (len(legal) > 0):
                    choice = random.randint(0,len(legal)-1)
                    move = legal[choice]
             #       move = self.getMove(legal)
                    self.makeMove(move)
                else:
                    print("No legal moves available, skipping turn...")
            else:
                legal = self.board.calcLegalMoves(self.turn)
                print("Valid Moves: ")
                for i in range(len(legal)):
                    print(str(i+1)+": ",end='')
                    print(str(legal[i].start)+" "+str(legal[i].end))
                if (len(legal)>0):
                    choice = random.randint(0,len(legal)-1)
                    self.makeMove(legal[choice])
                    print("Computer chooses ("+str(legal[choice].start)+", "+str(legal[choice].end)+")")
            # switch player after move
            self.turn = 1-self.turn
        print("Game OVER")
        print("Black Captured: "+str(NUM_PLAYERS-self.remaining[1]))
        print("White Captured: "+str(NUM_PLAYERS-self.remaining[0]))
        score = self.calcScore(self.board)
        print("Black Score: "+str(score[0]))
        print("White Score: "+str(score[1]))
        if (score[0] > score[1]):
              print("Black wins!")
        elif (score[1] > score[0]):
              print("White wins!")
        else:
            print("It's a tie!")
        self.board.drawBoardState()

    def makeMove(self, move):

        self.board.boardMove(move, self.turn)
        if move.jump:
            # decrement removed pieces after jump
            self.remaining[1-self.turn] -= len(move.jumpOver)
            print("Removed "+str(len(move.jumpOver))+" "+PLAYERS[1-self.turn]+" pieces")
  
    def getMove(self, legal):
        move = -1
        # repeats until player picks move on the list
        while move not in range(len(legal)):
            # List valid moves:
            print("Valid Moves: ")
            for i in range(len(legal)):
                print(str(i+1)+": ",end='')
                print(str(legal[i].start)+" "+str(legal[i].end))
            usr_input = input("Pick a move: ")
            # stops error caused when user inputs nothing
            move = -1 if (usr_input == '')  else (int(usr_input)-1)
            if move not in range(len(legal)):
                print("Illegal move")
        print("Legal move")
        return (legal[move])
    # returns a boolean value determining if game finished
    def gameOver(self):
        # all pieces from one side captured
        if (len(self.board.currPos[0]) == 0 or len(self.board.currPos[1]) == 0):
            return True
        # no legal moves available, stalemate
        elif (len(self.board.calcLegalMoves(0)) == 0 and len(self.board.calcLegalMoves(1)) == 0):
            return True
        else:
            # continue onwards
            return False
    #calculates the final score for the board
    def calcScore(self, board):
        score = [0,0]
        # black pieces
        for cell in range(len(board.currPos[0])):
            # black pieces at end of board - 2 pts
            if (board.currPos[0][cell][0] == 0):
                score[0] += 2
            # black pieces not at end - 1 pt
            else:
                score[0] += 1
        # white pieces
        for cell in range(len(board.currPos[1])):
            # white pieces at end of board - 2 pts
            if (board.currPos[1][cell][0] == BOARD_SIZE-1):
                score[1] += 2
            # white pieces not at end - 1 pt
            else:
                score[1] += 1
        return score

        
        

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
  #      print(self.currPos[currPlayer])

    def calcLegalMoves(self, player): # int array  -> [0] reg, [1] jump
        legalMoves = []
        hasJumps = False
        # next goes up if black or down if white
        next = -1 if player == 0 else 1
        boardLimit = 0 if player == 0 else 7
        # cell refers to a position tuple (row, col)
        for cell in self.currPos[player]:
            if (cell[0] == boardLimit):
                continue
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

    # enemy is the square we plan to jump over
    # change later to deal with double jumps
    def checkJump(self, cell, isLeft, player):
        jumps = []
        next = -1 if player == 0 else 1
        # check boundaries!
        if (cell[0]+next == 0 or cell[0]+next == BOARD_SIZE-1):
            return jumps
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
    # uncomment this when its time to try double jumps
    #    print("Jumps:")
    #    for mov in jumps:
    #        print(str(mov.start)+" "+str(mov.end)+" Jump over: "+str(mov.jumpOver))
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
