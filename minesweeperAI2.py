import numpy as np
import random

class AI2():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

        self.queue = []
        self.dontOpen = []
        self.bombs = []
        self.digs = []

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState):
        print(boardState)

        # If there are squares in the queue, we already know another square that is a bomb
        if len(self.queue) > 0:
            squareToOpen = self.queue.pop()
            self.digs.append(squareToOpen)
            print(f"Square to open is {squareToOpen}")
            return self.open_square_format(squareToOpen)

        # Find all opened and unopened squares, and update bomb list
        openedSquares = []
        unopenedSquares = []
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1:
                    unopenedSquares.append((row, col))
                elif boardState[row][col] != 9:
                    openedSquares.append((row, col))
                else:
                    if (row, col) not in self.bombs:
                        self.bombs.append((row, col))
                    if (row, col) not in openedSquares:
                        openedSquares.append((row, col))

        # If number of bombs found equals total number of bombs on the board, we're done
        if len(self.bombs) == self.numBombs:
            print(f"List of bombs is {self.bombs}")
            print(self.digs)
            return self.submit_final_answer_format(self.bombs)

        else:
            maxProb = 0
            maxSquare = None
            maxUnrevealed = []

            for square in openedSquares:
                row = square[0]
                col = square[1]

                # Assign outerSquares based on edge case
                if row == 0 and col == 0:
                    outerSquares = [(0, 1), (1, 0), (1, 1)]
                elif row == 0 and col == self.numCols - 1:
                    outerSquares = [(0, self.numCols - 2), (1, self.numCols - 2), (1, self.numCols - 1)]
                elif row == self.numRows - 1 and col == 0:
                    outerSquares = [(self.numRows - 2, 0), (self.numRows - 2, 1), (self.numRows - 1, 1)]
                elif row == self.numRows - 1 and col == self.numCols - 1:
                    outerSquares = [(self.numRows - 2, 0), (self.numRows - 2, 1), (self.numRows - 1, 1)]
                elif row == 0:
                    outerSquares = [(0, col - 1), (0, col + 1), 
                                    (1, col - 1), (1, col), (1, col + 1)]
                elif row == self.numRows - 1:
                    outerSquares = [(self.numRows - 1, col - 1), (self.numRows - 1, col + 1), 
                                    (self.numRows - 2, col - 1), (self.numRows - 2, col), (self.numRows - 2, col + 1)]
                elif col == 0:
                    outerSquares = [(row - 1, 0), (row + 1, 0), 
                                    (row - 1, 1), (row, 1), (row + 1, 1)]
                elif col == self.numCols - 1:
                    outerSquares = [(row - 1, self.numCols - 1), (row + 1, self.numCols - 1), 
                                    (row - 1, self.numCols - 2), (row, self.numCols - 2), (row + 1, self.numCols - 2)]
                else:
                    outerSquares = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                                    (row, col - 1), (row, col + 1),
                                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

                # Calculate probability and unrevealed squares for center square
                prob, unrevealed = self.calculateProb(square, outerSquares, boardState)

                # All squares surrounding center square are already opened 
                if prob is None or unrevealed is None:
                    continue

                # If we know that the surrounding squares must be bombs
                if prob == 1:
                    squareToOpen = unrevealed[0]
                    if len(unrevealed) > 1:
                        self.queue += unrevealed[1:]
                    self.digs.append(squareToOpen)
                    print(f"Square to open is {squareToOpen}")
                    return self.open_square_format(squareToOpen)
                
                # If we know that the surrounding squares are safe, we don't want to open them
                if prob == 0:
                    self.dontOpen += unrevealed
                
                # Update square with highest probability of having a bomb surrounding it
                if prob > maxProb:
                    maxProb = prob
                    maxSquare = square
                    maxUnrevealed = unrevealed


            # Pick random square from the unrevealed squares surrounding the center square with highest probability
            for squareToOpen in maxUnrevealed:
                if squareToOpen not in self.dontOpen:
                    self.digs.append(squareToOpen)
                    print(f"Square to open is {squareToOpen}")
                    return self.open_square_format(squareToOpen)
            

            # Last resort is to pick a random square on the grid.
            # Make sure the random square isn't one that you know isn't a bomb
            squareToOpen = random.choice(unopenedSquares)
            while squareToOpen in self.dontOpen:
                squareToOpen = random.choice(unopenedSquares)
            self.digs.append(squareToOpen)
            print(f"Square to open is {squareToOpen}")
            return self.open_square_format(squareToOpen)
    

    # Calculate the probability that a surrounding square in centerSquare's vicinity is a bomb
    # centerSquare: square we want to calculate probability for
    # outerSquares: squares surrounding the centerSquare
    # Probability = ((center number) - (# of bombs)) / (# of unopened squares)
    def calculateProb(self, centerSquare, outerSquares, boardState):
        centerNum = boardState[centerSquare[0], centerSquare[1]]
        bombCount = 0
        unopenedCount = 0
        unrevealed = []

        for square in outerSquares:
            squareNum = boardState[square[0], square[1]]
            # Count number of known bombs
            if squareNum == 9:
                bombCount += 1
            # Count number of unopened squares
            elif squareNum == -1:
                # If we already know a square isn't a bomb, we won't count it for unopenedCount
                if square not in self.dontOpen:
                    unopenedCount += 1
                unrevealed.append(square)
        
        # If all outer squares are opened, return None to ignore center square
        if unopenedCount == 0:
            return None, None
        
        # Return probability that a square is a bomb
        return (centerNum - bombCount) / unopenedCount, unrevealed

