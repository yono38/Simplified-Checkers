Simplified-Checkers
===================

Simplified Version of Checkers for a school project

No kinging, game ends when no more moves or all opponents pieces captured
The point of the project is to implement AI with alpha-beta pruning

Running the program:
To run the program, install python 3.0 or higher (http://www.python.org/download/releases/3.2.3/) and run the command python3 checkers.py

High-level design:
I designed the game as a set of classes that would abstract the various aspects of the program. Globals were used to define the board size, number of players, depth limit, and the array of different players (“Black” and “White”). 

I used the following classes:
Game
-contains the most high level aspects of the game
-maintains the state of the turn, which color the player is playing, etc
-deals with move input from the user
-determines if game over and calculates score
-contains the alpha-beta function
AB_Value
-used to contain statistics of the alpha-beta function
-move_value - the “v” from the original algorithm, an integer
-move - contains an action in the form of a move class
-max-depth - an int of the max depth travelled by the tree so far
-nodes - an int totalling the current node and all it’s children
-max-cutoff - an int tracking the number of cutoffs in the max function
-min-cutoff - an int tracking the number of cutoffs in the min function
AB_State
-used to pass the simulated game state through the alpha-beta function
-board - state of the board at that node
-player - current player at that node (black or white)
Move
-contains info required to make a move
-board postitions are contained in arrays with [row number, column number]
-start - contains a start position for a piece in the form of position array
-end - contains a end position for a piece in the form of position array
-jump - boolean determining whether a piece was a jump or just a basic move
-jumpOver - an array of enemy piece positions that were jumped over
Board
-contains info on state of the board independent of the game itself
-boardState - a multidimensional array containing the state of the board; for each boardState[row][col], the value is one of the following:
-- 1 - board is empty on this position
-- 0 - board has black piece on this position
-- 1 - board has white piece on this position
-calcLegalMoves – takes input of current player and returns array of valid moves for that player
--if any jumps are available, it only returns jumps
-checkJump – checks a board piece to see if can make any jumps
-calcPos – returns array containing current board positions of all black and white pieces
-drawBoardState – turns the boardState array into lines of text made of B, W, and +

Terminal State Utility Values:
For the terminal state, if the original player (the computer) had a winning position, I did 100 + (Computer Final Score – Player Final Score). If the computer lost, I did -100 + (Computer Final Score – Player Final Score).

Non-Terminal State Evaluation Function:
For each black and white I did the following calculations:
+7 if the piece was in the opposite player's end
+5 if the piece was in the opposite player's half of the board
+3 if the piece was in the player's own half of the board

I would then calculate (total score of computer's pieces – total score of player's pieces) to get the number of pieces on the board. This heuristic results in a very aggressive strategy by the computer, causing it to try to move as many pieces to the player's end as possible without having them captured. This emphasis estimates the final goal, having as many uncaptured pieces as possible on the other side of the board while minimizing the player's pieces on their side.

Runs pretty slowly because of the deep copies of my board required for each level of the minimax. If I were to write this again I would implement it more efficiently.
