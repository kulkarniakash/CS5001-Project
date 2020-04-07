''' CS5001 Project
    Spring 2020
    Akash Kulkarni

    Driver file
    Note: remember to shift all class definitions to different files
    before production!

    The Difficulty is set to 4 for single player mode. This may cause a slight
    delay in the response of the computer after the human has played (2-4 seconds)
    . For as faster albeit easier gaming experience, please adjust the difficulty\
    to a lower level.
'''
import turtle
from button import ButtonManager, Button
from game import Game

MAX_WIDTH = 12
MAX_HEIGHT = 12



# create two buttons, prompting user to choose between two player or one player        
        

def createTwoPlayerGame(width, height):
    ''' Parameters: none
        Return: none
        Creates a two player game
    '''
    initializeGame(False, (height, width))

def createSinglePlayerGame(width, height):
    ''' Parameters: none
        Return: none
        Creates a single player game
    '''
    screen = turtle.Screen()
    screen.clear()
    
    playFirst = Button((-100,30), "Play First (Red)",
                       lambda x,y: initializeGame(True, (height, width)))
    playSecond = Button((-140,-30), "Play Second (Yellow)",
                        lambda x,y: initializeGame(True, (height, width),
                                         compPlaysFirst=True))
    playFirst.drawButton()
    playSecond.drawButton()
    buttonManager = ButtonManager([playFirst, playSecond])
    buttonManager.initializeScreen()

def initializeGame(isSinglePlayer, size, compPlaysFirst=False):
    
    newGame = Game(isSinglePlayer, size, compPlaysFirst)
    newGame.initializeScreen()
    newGame.loadScores()
    newGame.displayScores()
    newGame.initializeBoard()
    newGame.renderBoard((newGame.h_holes, newGame.w_holes))



def main():

    option = input("Hey! Welcome to Connect 4. The default size of the board is"
                   " 6x7. Would you like to change it? (y/n)\n")
    while option not in ["y", "Y", "n", "N"]:
        option = input("Invalid response, please enter (y/n):\n")
        
    width = 7
    height = 6
    if option in ["y", "Y"]:
        width = int(input("How many horizontal holes (2-" + str(MAX_WIDTH) + ")?\n"))
        while width not in range(2, MAX_WIDTH+1):
            width = int(input("Sorry, that's not in range. Please type again:\n"))
        height = int(input("How many vertical holes (2-" + str(MAX_HEIGHT) + ")?\n"))
        while height not in range(2, MAX_HEIGHT+1):
            height = int(input("Sorry, that's not in range. Please type again:\n"))

    

    singlePlayer = Button((-100,30), "Single Player",
                          lambda x,y: createSinglePlayerGame(width, height))
    twoPlayer = Button((-80,-30), "Two Player",
                          lambda x,y: createTwoPlayerGame(width, height))

    singlePlayer.drawButton()
    twoPlayer.drawButton()
    
    buttonManager = ButtonManager([singlePlayer, twoPlayer])
    buttonManager.initializeScreen()
        
main()


