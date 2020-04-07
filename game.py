''' CS5001- Project
    game.py
    Akash Kulkarni

    contains the game class, which consists of all essential components of the
    main game like rendering the board, handling click events for coins,
    calculating strategic moves for the computer to make, etc.
'''

from button import ButtonManager, Button
import turtle
import time
import copy
import random

DIFFICULTY = 4

class Game:
    def __init__(self, isSinglePlayer, size=(6,7), compPlaysFirst=False):
        ''' Parameters: size of board (in number of circles) -tuple (height,
            width), whether the game is single player or not -bool
            Red gets to play first by default
        '''
        
        self.buttonManager = None
        self.sequenceOfMoves = []
        self.compPlaysFirst = compPlaysFirst
        self.isCompTurn = True if compPlaysFirst else False
        # values of every filled hole on the board
        self.board = []
        # indicates whose turn it is, choices- "r" or "y", change to alternate
        # every game
        self.toPlay = "r"
        # height and width of board in number of holes
        self.h_holes = size[0]
        self.w_holes = size[1]
        # radius of hole
        self.radius = 30
        # space between two holes
        self.space = 5
        # color of the board
        self.boardColor = "blue"
        # width and height of the board calculated in pixels
        self.width = self.w_holes * (2 * self.radius) + (self.w_holes + 1) * \
                     (self.space)
        self.height = self.h_holes * (2 * self.radius) + (self.h_holes + 1) * \
                      (self.space)
        # if the coin drop animation is still running, we don't want any
        # additional clicks to be handled
        self.isAnimating = False
        self.isSinglePlayer = isSinglePlayer
        self.winner = ""
        # number of coins on the board
        self.coinsPlayed = 0
        # turtle for the displayTurn function
        self.displayTurnTurtle = None# turtle.Turtle()
        # self.displayTurnTurtle.ht()
        # name of file that stores the score
        self.filename = "score.txt"
        # scores of yellow and red
        self.redScore = 0
        self.yellowScore = 0
        
        
        
        

    def initializeScreen(self):
        screen = turtle.Screen()
        screen.onclick(None)
        screen.clear()
        screen.setup(width=self.width+400, height=self.height+400)
        self.displayTurnTurtle = turtle.Turtle()
        self.displayTurnTurtle.ht()
        self.displayTurn()
        
        rewind = Button((self.width/2 + 20, 0), "Rewind", lambda x,y:\
                        self.rewind(x,y))
        rewind.drawButton()
        
        self.buttonManager = ButtonManager([rewind])
        self.buttonManager.initializeScreen()
        
        

    def loadScores(self):
        ''' Parameters: none
            Return: none
            loads scores from file with name self.filename
            scores are stored in the format r: 0 y: 0
        '''
        try:
            with open(self.filename, "r") as infile:
                content = infile.readlines()[0].split()
                self.redScore = int(content[1])
                self.yellowScore = int(content[3])
        except OSError:
            print("Could not read scores from file, both scores are now zero")

    def writeScores(self):
        ''' Parameters: none
            Return: none
            writes updated score to file if one player wins
        '''
        
        try:
            with open(self.filename, "w") as outfile:
                if self.winner == "r":
                    outfile.write("r: " + str(self.redScore+1) + " y: " +\
                                  str(self.yellowScore))
                elif self.winner == "y":
                    outfile.write("r: " + str(self.redScore) + " y: " +\
                                  str(self.yellowScore+1))
        except OSError:
            Print("Sorry, could not save your score")

    def displayScores(self):
        ''' Parameters: none
            Return: none
            displayes the current score on the screen
        '''
        textTurtle = turtle.Turtle()
        textTurtle.ht()
        textTurtle.up()
        textTurtle.goto(0, self.height/2 + 100)
        textTurtle.color("red")
        textTurtle.write("Red: " + str(self.redScore) +"   ", align="right", move=True,
                         font = ("Arial", 24, "normal"))
        textTurtle.color("yellow")
        textTurtle.write("  Yellow: " + str(self.yellowScore), align="left",
                         font = ("Arial", 24, "normal"))
            
    def initializeBoard(self):
        ''' Parameters: none
            Return: none
            Initializes board with empty lists
        '''
        for i in range(self.w_holes):
            self.board.append([])
        

    def rewind(self, x, y):
        
        if not self.sequenceOfMoves or self.winner or self.isAnimating:
            return
        if self.isSinglePlayer and len(self.sequenceOfMoves) < 2:
            return
        if not self.isSinglePlayer:
            self.toPlay = "r" if self.toPlay == "y" else "y"
        self.eraseLastCoin(self.sequenceOfMoves[-1])
        self.board[self.sequenceOfMoves[-1]].pop()
        self.sequenceOfMoves.pop()
        if self.isSinglePlayer:
            self.eraseLastCoin(self.sequenceOfMoves[-1])
            self.board[self.sequenceOfMoves[-1]].pop()
            self.sequenceOfMoves.pop()

            
        
##    def handleCompsTurnClick(self, x, y):
##        thinkingTurtle = turtle.Turtle()
##        thinkingTurtle.ht()
##        thinkingTurtle.up()
##        thinkingTurtle.goto(0, -self.height/2-40)
##        thinkingTurtle.write("Wait, computer is thinking",align="center",
##                                     font=("Arial", 24, "normal"))
##        self.handleCoinDrop(0, 0, self.compMove())
##        thinkingTurtle.clear()
##        self.compsTurn.buttonTurtle.clear()
##        self.compsTurn.callback = lambda x,y: 1
##        if len(self.buttonManager.buttons) == 2:
##            self.buttonManager.buttons.pop()
##        self.isCompTurn = False

    def eraseLastCoin(self, buttonNumber):

        screen = turtle.Screen()
        i = self.h_holes - len(self.board[buttonNumber]) + 1
        myCoin = turtle.Turtle()
        myCoin.ht()
        myCoin.up()
        myCoin.fillcolor("white")
        myCoin.lt(90)
        x = -self.width/2 + (buttonNumber+1) * (2 * (self.radius) + \
                        self.space) 
        y = self.height/2 - 2 * i * (self.radius) - i * self.space \
                + self.radius
        myCoin.goto(x, y)
        myCoin.down()
        myCoin.begin_fill()
            
        myCoin.circle(self.radius)
        myCoin.end_fill()

        self.displayTurn()
        screen.update()
        
        

    def displayTurn(self):
        ''' Parameters: none
            Return: none
            displays on the screen whose turn it is
        '''
        self.displayTurnTurtle.clear()
        self.displayTurnTurtle.up()
        self.displayTurnTurtle.goto(-self.width/2 - 100, 0)
        if self.toPlay == "r":
            self.displayTurnTurtle.color("red")
            self.displayTurnTurtle.write("Red's turn!", align="center", font=\
                              ("Arial", 24, "normal"))
        elif self.toPlay == "y":
            self.displayTurnTurtle.color("yellow")
            self.displayTurnTurtle.write("Yellow's turn!", align="center", font=\
                              ("Arial", 24, "normal"))

    def displayWinner(self):
        ''' Parameters: none
            Return: none
            Displays the winner
        '''
        self.displayTurnTurtle.clear()
        textTurtle = turtle.Turtle()
        textTurtle.ht()
        textTurtle.up()
        textTurtle.goto(0, -self.height/2 - 50)
        if self.winner == "r":
            textTurtle.color("red")
            textTurtle.write("Red is the winner!!", align="center", font=\
                             ("Arial", 24, "normal"))
        elif self.winner == "y":
            textTurtle.color("yellow")
            textTurtle.write("Yellow is the winner!!", align="center", font=\
                             ("Arial", 24, "normal"))

    def displayDraw(self):
        ''' Parameters: none
            Return: none
            Displays "draw message"
        '''

        self.displayTurnTurtle.clear()
        textTurtle = turtle.Turtle()
        textTurtle.ht()

        textTurtle.up()
        textTurtle.goto(0, -self.height/2 - 50)
        textTurtle.write("It's a Draw!", align="center", font=\
                        ("Arial", 24, "normal"))

    def fetchWinner(self, buttonNumber):
        ''' Parameters: which was the last button pressed- int
            Return:
            Checks to see if there is a winner on the board
        '''
        # denote how many coins of the same color are there in a row,
        # horizontal, vertical, main diagonal, other diagonal
        hor = 0
        vert = 0
        maind = 0
        otherd = 0

        i = 1
        index_x = buttonNumber
        index_y = len(self.board[buttonNumber])-1
        def overflowCheck():
            return index_x in range(0, self.w_holes) and\
                   index_y in range(0, len(self.board[index_x])) and\
                   self.board[index_x][index_y] == self.toPlay
        # check the horizontal for coins
        while i <= 4 and overflowCheck():
            hor += 1
            index_x -= 1
            i += 1

        i = 1
        index_x = buttonNumber + 1
        index_y = len(self.board[buttonNumber])-1

        while i <= 4 and overflowCheck():
            hor += 1
            index_x += 1
            i += 1

        # check the vertical for coins
        i = 1
        index_x = buttonNumber
        index_y = len(self.board[buttonNumber])-1

        while i <= 4 and overflowCheck():
            vert += 1
            index_y -= 1
            i += 1

        # check the main diagonal for coins
        i = 1
        index_x = buttonNumber
        index_y = len(self.board[buttonNumber]) - 1
        
        while i <= 4 and overflowCheck():
            maind += 1
            index_y += 1
            index_x -= 1
            i += 1

        i = 1
        index_x = buttonNumber + 1
        index_y = len(self.board[buttonNumber]) - 2
        
        while i <= 4 and overflowCheck():
            maind += 1
            index_y -= 1
            index_x += 1
            i += 1

        # check the other diagonal for coins
        i = 1
        index_x = buttonNumber
        index_y = len(self.board[buttonNumber]) - 1
        
        while i <= 4 and overflowCheck():
            otherd += 1
            index_y += 1
            index_x += 1
            i += 1

        i = 1
        index_x = buttonNumber-1
        index_y = len(self.board[buttonNumber]) - 2
        
        while i <= 4 and overflowCheck():
            otherd += 1
            index_y -= 1
            index_x -= 1
            i += 1

        if max([hor, vert, otherd, maind]) >= 4:
            self.winner = self.toPlay
            
    def compMove(self):
        ''' Parameters: none
            Return: move -int 
            returns which hole the computer chooses
        '''

        return self.winningMoves(copy.copy(self.board), DIFFICULTY, 0)  # legalMoves[0] #random.randint(0, self.w_holes-1)

    # strategy is a brute force method to create a tree of possibilities
    # and choosing that path which leads to a win. A path can be classified
    # as either a regular win, or a strong win, one where the opponent at
    # some point, is forced to concede as there is no option but victory for
    # the computer

    def winningMoves_aux(self, board, depth, level):
        # list of wins depending on which index the computer chooses
        
        wins = 0
        turn = ""
        if self.compPlaysFirst:
            turn = "r" if level%2 != 0 else "y"
        else:
            turn = "y" if level%2 != 0 else "r"
        if level > depth:
            return 0
        opp = "r" if turn == "y" else "y"
        size = 0
        for col in board:
                size += len(col)
        if size == self.w_holes * self.h_holes:
                return 0
            
        
            
        for move in range(0, self.w_holes):
            if len(board[move]) > self.h_holes:
                return 0
            
            # create a deep copy of board
            board_copy = []
            for col in self.board:
                board_copy.append(copy.copy(col))
            # check for any winner, remember to reset self.toPlay
            # and self.board and self.winner!
            self.toPlay = turn
            self.board = board

            self.fetchWinner(move)
            
            self.toPlay = "r" if self.compPlaysFirst else "y"
            # copying back the original board
            self.board = []
            for col in board_copy:
                self.board.append(copy.copy(col))
                
            winner = self.winner
            self.winner = ""
            
            board_copy = []
            for col in board:
                board_copy.append(copy.copy(col))

            
            if winner == ("r" if self.compPlaysFirst else "y"):
                wins += 1 * (depth - level + 1)
            elif winner != "":
                #NEW CODE
                if level == 2:
                    return -1000
                wins -= 1 * (depth - level + 1) 
            else:
                board_copy[move].append(turn)
                wins += self.winningMoves_aux(board_copy, depth, level+1)

        
        return wins

    def winningMoves(self, board, depth, level):

        wins = {}
        turn = "r" if self.compPlaysFirst else "y"
        self.isAnimating = True
        board = []
        for col in self.board:
            board.append(copy.copy(col))
        
        for i in range(0, self.w_holes):
            if len(board[i]) >= self.h_holes:
                continue
            board[i].append(turn)

            temp = self.board
            self.board = []
            for col in board:
                self.board.append(copy.copy(col))

            self.fetchWinner(i)
            if self.winner == turn:
                self.board = temp
                self.winner = ""
                self.isAnimating = False
                return i
            self.board = temp
            self.winner = ""
            wins[i] = self.winningMoves_aux(board, depth, level)
            board[i].pop()
        
        maximum = min(wins.keys())
        for i in wins:
            if wins[i] > wins[maximum]:
                maximum = i
        self.isAnimating = False
        return maximum
        

    
    def addCoinToBoard(self, buttonNumber):
        ''' Parameters: which button was pressed -int (range: 1-self.w_holes)
            Return: none
            Add the appropriate coin to self.board in the correct slot
        '''
        self.board[buttonNumber].append(self.toPlay)
        self.sequenceOfMoves.append(buttonNumber)
        self.coinsPlayed += 1
        self.fetchWinner(buttonNumber)
        

    def pause(self, seconds):
        then = time.time()
        while(time.time()-then < seconds):
            pass

    def dropAnimation(self, buttonNumber):
        ''' Parameters: which button was pressed -int (range: 1 - self.w_holes)
            Return: none
            Show animation of coin dropping
        '''
        self.isAnimating = True
        screen = turtle.Screen()
        myCoin = turtle.Turtle()
        myCoin.ht()
        myCoin.fillcolor("red" if self.toPlay == "r" else "yellow")
        myCoin.lt(90)
        print(self.w_holes, "self.h_holes")
        for i in range(1, self.h_holes - len(self.board[buttonNumber])+2):
            myCoin.up()
            myCoin.clear()
            x = -self.width/2 + (buttonNumber+1) * (2 * (self.radius) + \
                        self.space) 
            y = self.height/2 - 2 * i * (self.radius) - i * self.space \
                + self.radius
            myCoin.goto(x, y)
            myCoin.down()
            myCoin.begin_fill()
            
            myCoin.circle(self.radius)
            myCoin.end_fill()  
            screen.update()
            if i != self.h_holes - len(self.board[buttonNumber]) + 1:
                self.pause(0.05)
        self.isAnimating = False

        

    def handleCoinDrop(self, x, y, move=-1):
        ''' Paramters: x , y -integers, position of click, move of computer,
            if it's the computer's turn
            Return: none
            handles click event of black triangles
        '''
        
        buttonNumber = move
        if self.winner != "" or self.coinsPlayed == self.w_holes*self.h_holes:
            return
        if move == -1:
            buttonNumber = (x + self.width/2) // (self.space + 2 * self.radius)
                   
        if len(self.board[int(buttonNumber)]) < self.h_holes and not self.isAnimating\
           and not (self.isCompTurn and move == -1):
            print(self.board)
            # adds the data of the coin dropped to self.board
            self.addCoinToBoard(int(buttonNumber))
            # renders graphics of coin drop
            self.dropAnimation(int(buttonNumber))
            if self.winner != "":
                self.displayWinner()
                self.writeScores()
                return
            elif self.coinsPlayed == self.w_holes * self.h_holes:
                self.displayDraw()
                return
            
            self.toPlay = "y" if self.toPlay == "r" else "r"
        self.displayTurn()
        
        if self.isSinglePlayer and not (self.isCompTurn and move == -1):
            compPlays = (self.compPlaysFirst and self.toPlay == "r") or \
                        (not self.compPlaysFirst and self.toPlay == "y")
            if compPlays:
                self.isCompTurn = True
                thinkingTurtle = turtle.Turtle()
                thinkingTurtle.ht()
                thinkingTurtle.up()
                thinkingTurtle.goto(0, -self.height/2-40)
                thinkingTurtle.write("Wait, computer is thinking",align="center",
                                     font=("Arial", 24, "normal"))
                self.handleCoinDrop(0, 0, move=self.compMove())
                thinkingTurtle.clear()
                self.isCompTurn = False
            else:
                return
            
        

    def renderBoard(self, size):
        ''' Parameters: size of board (in number of circles) -tuple (height,
            width)
            Note: use tracer and update to hide animation of turtle
        '''
        
        loadTextTurtle = turtle.Turtle()
        loadTextTurtle.ht()
        loadTextTurtle.write("Loading Board", align="center",
                             font=("Arial", 24, "normal"))
        screen = turtle.Screen()
        screen.tracer(0)
        
        boardTurtle = turtle.Turtle()
        boardTurtle.fillcolor(self.boardColor)
        boardTurtle.up()
        boardTurtle.goto(-self.width/2, self.height/2)
        boardTurtle.down()

        boardTurtle.begin_fill()
        boardTurtle.fd(self.width)
        boardTurtle.rt(90)
        boardTurtle.fd(self.height)
        boardTurtle.rt(90)
        boardTurtle.fd(self.width)
        boardTurtle.rt(90)
        boardTurtle.fd(self.height)
        boardTurtle.end_fill()

        boardTurtle.fillcolor("white")

        for i in range(1, self.h_holes+1):
            for j in range(1, self.w_holes + 1):
                boardTurtle.up()
                x = -self.width/2 + j * (self.space + 2 * self.radius)
                y = -self.height/2 + i * (self.space + 2 * self.radius) - self.radius
                boardTurtle.goto(x, y)
                boardTurtle.down()
                boardTurtle.begin_fill()
                boardTurtle.circle(self.radius)
                boardTurtle.end_fill()
        boardTurtle.ht()

        if self.isSinglePlayer and self.compPlaysFirst:
            self.handleCoinDrop(0, 0, move=self.compMove())
            self.isCompTurn = False
            
        screen.register_shape("triangle", ((-self.radius/2, 0),(self.radius/2,0), (0, -40)))
        for i in range(1, self.w_holes+1):
            myTurtle = turtle.Turtle(shape="triangle")
            myTurtle.up()
            x = -self.width/2 + i * (self.space + 2 * self.radius) - self.radius
            y = self.height/2 + 60
            myTurtle.goto(x, y)
            myTurtle.lt(90)
            myTurtle.onclick(self.handleCoinDrop)

        loadTextTurtle.clear()
        screen.update()
