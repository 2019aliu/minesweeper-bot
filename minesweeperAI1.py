import numpy as np
import random


class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows"
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

        self.questionableQueue = set()
        self.probedQueue = set()

        self.unopenedSquares = set()
        self.bombsFoundSoFar = set()

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    def performAI(self, boardState):
        print(boardState)

        if len(self.bombsFoundSoFar) == 0:
            for row in range(self.numRows):
                for col in range(self.numCols):
                    if boardState[row][col] == -1:
                        self.unopenedSquares.add((row, col))
                    elif boardState[row][col] == 9:
                        self.bombsFoundSoFar.add((row, col))

        if len(self.bombsFoundSoFar) == self.numBombs:
            # If the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            print(f"List of bombs is {self.bombsFoundSoFar}")
            return self.submit_final_answer_format(self.bombsFoundSoFar)
        else:
            preProbe = self.probeIfNeeded()
            if preProbe:
                return preProbe

            # process information from the previously opened square
            # it may be a bomb or it may have a "0"
            # otherwise, we just add it to be processed later when we have more info
            while len(self.probedQueue) > 0:
                # process the sample from the previous move (saved state)
                sample = self.probedQueue.pop()
                self.unopenedSquares.remove(sample)
                if boardState[sample[0]][sample[1]] == 9:
                    self.bombsFoundSoFar.add(sample)

                UN = set()
                UN = self.unmarkedNeighbors(
                    sample[0], sample[1], False)
                # all neighboring squares are safe
                if boardState[sample[0]][sample[1]] == 0:
                    for item in UN:
                        self.unopenedSquares.remove(item)
                # not enough info yet, push to Q
                else:
                    self.questionableQueue.add(sample)

            deletionSet = set()
            # process the "questionable" squares without opening to see if we have enough information to infer anything
            # 2 strategies: either we know all neighboars are mines, or we know all neighbors are clear
            # otherwise, keep the square as questionable, we might know more later
            for sample in self.questionableQueue:
                UN = set()
                UN = self.unmarkedNeighbors(
                    sample[0], sample[1], True)
                # all neighboring squares are mines
                if boardState[sample[0]][sample[1]] == len(UN):
                    for item in UN:
                        if not(item in self.bombsFoundSoFar):
                            self.bombsFoundSoFar.add(item)
                            self.unopenedSquares.remove(item)
                    deletionSet.add(sample)
                # all neighboring squares are safe
                if boardState[sample[0]][sample[1]] == 0:
                    UN = self.unmarkedNeighbors(
                        sample[0], sample[1], False)
                    for item in UN:
                        self.unopenedSquares.remove(item)
                    deletionSet.add(sample)

            # remove all processed squares
            # avoids python error
            for item in deletionSet:
                self.questionableQueue.remove(item)

            # some debug fun
            print(self.unopenedSquares)

            postProbe = self.probeIfNeeded()
            if postProbe:
                return postProbe

    # opens the square if there are no more elements to process from the previous move
    # will run either at the start of the move or at the end
    # the idea is that no matter what we do during the move itself, at the end of the day we still have to open some random square
    def probeIfNeeded(self):
        if len(self.probedQueue) == 0:
            squareToOpen = random.sample(self.unopenedSquares, 1)[0]
            self.probedQueue.add(squareToOpen)
            return self.open_square_format(squareToOpen)

    # determines which neighbors of a given square have not been opened yet
    def unmarkedNeighbors(self, row, col, includesBombs):
        UN = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    item = (row - i, col - j)
                    if (item in self.unopenedSquares) or (includesBombs and item in self.bombsFoundSoFar):
                        UN.add(item)
        return UN
