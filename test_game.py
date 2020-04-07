''' CS5001-Project
    test_game.py
    Akash Kulkarni

    Tests most functions in game.py that exclusively deal with the functionality
    of the game as opposed to graphics.
'''

from game import Game
from button import ButtonManager, Button
import unittest

class GameTest(unittest.TestCase):
    def test_init(self):
        obj = Game(True, (7, 9), True)
        self.assertEqual(obj.buttonManager, None)
        self.assertEqual(obj.sequenceOfMoves, [])
        self.assertTrue(obj.compPlaysFirst)
        self.assertTrue(obj.compPlaysFirst)
        self.assertEqual(obj.board, [])
        self.assertEqual(obj.toPlay, "r")
        self.assertEqual(obj.h_holes, 7)
        self.assertEqual(obj.w_holes, 9)
        self.assertEqual(obj.radius, 30)
        self.assertEqual(obj.space, 5)
        self.assertEqual(obj.boardColor, "blue")
        self.assertEqual(obj.width, 590)
        self.assertEqual(obj.height, 460)
        self.assertFalse(obj.isAnimating)
        self.assertTrue(obj.isSinglePlayer)
        self.assertEqual(obj.winner, "")
        self.assertEqual(obj.coinsPlayed, 0)
        self.assertEqual(obj.displayTurnTurtle, None)
        self.assertEqual(obj.filename, "score.txt")
        self.assertEqual(obj.redScore, 0)
        self.assertEqual(obj.yellowScore, 0)

    def test_loadScores(self):
        # we first create a new file with name self.filename and then
        # read from it using the loadScores function
        obj = Game(True)
        obj.filename = "scores_test_read"
        try:
            with open(obj.filename, "w") as outfile:
                outfile.write("r: 234 y: 45")
            obj.loadScores()
            self.assertEqual(obj.redScore, 234)
            self.assertEqual(obj.yellowScore, 45)
        except OSError:
            print("Error: could not test Game.loadScores()")

    def test_writeScores(self):
        # we first write using Game.writeScores and then read contents
        # to verify values
        obj = Game(True)
        obj.redScore = 23
        obj.yellowScore = 40
        # writeScores will increment the winner's score, in this case,
        # red's
        obj.winner = "r"
        obj.filename = "scores_test_write"
        obj.writeScores()
        try:
            content = None
            with open(obj.filename, "r") as infile:
                content = infile.readlines()[0]
            self.assertEqual(content, "r: 24 y: 40")
        except OSError:
            print("Error: could not test Game.writeScores()")
            
    def test_initializeBoard(self):
        # 7 and 8 are the height and width respectively
         obj = Game(True, (7,8))
         obj.initializeBoard()
         self.assertEqual(obj.board, [[],[],[],[],[],[],[],[]])

    def test_fetchWinner(self):
        obj = Game(True)
        # the player who last played
        obj.toPlay = "y"
        obj.board = [["r", "r", "r", "y"], ["y"], ["y"], [], [], [], []]
        obj.fetchWinner(0)
        self.assertEqual(obj.winner, "")

        obj = Game(False)
        # the player who last played
        obj.toPlay = "r"
        obj.board = [["r", "r", "r", "r"], ["y"], ["y"], ["y"], [], [], []]
        obj.fetchWinner(0)
        self.assertEqual(obj.winner, "r")

        obj = Game(True)
        # the player who last played
        obj.toPlay = "r"
        obj.board = [["r", "y"], ["r", "y"], ["r", "y"], ["r"], [], [], []]
        obj.fetchWinner(3)
        self.assertEqual(obj.winner, "r")

        obj = Game(True)
        # the player who last played
        obj.toPlay = "r"
        obj.board = [["r"], ["y", "r"], ["y", "y", "r"],
                     ["r", "y", "r", "r"], ["y"], [], []]
        obj.fetchWinner(3)
        self.assertEqual(obj.winner, "r")

    def test_compMove(self):
        # this partiucular function is slightly difficult to test since it create
        # trees that assign numbers proportional to the probability of a win, but
        # there are a few situations under which certain results should be expected
        # In all the testcases, the comp plays second and is yellow

        # this particular test case is interesting since there is both the possibility
        # of defeat and victory in the next set of moves. The program has been written
        # such that if there is a possibility of victory in the very next move, it ignores
        # all possiblities of defeat
        obj = Game(True)
        # player whose turn it currently is
        obj.toPlay = "y"
        obj.isCompTurn = True
        obj.board = [["r"], ["y", "r"], ["y", "r"], ["y", "r"], [], [], []]
        self.assertEqual(obj.compMove(), 4)

        # thwarting imminent victory of opponent
        obj = Game(True)
        # player whose turn it currently is
        obj.toPlay = "y"
        obj.isCompTurn = True
        obj.board = [[], ["y"], ["y"], [], [], ["r", "r", "r"], []]
        self.assertEqual(obj.compMove(), 5)

        # thwarting imminent victory of opponent
        obj = Game(True)
        # player whose turn it currently is
        obj.toPlay = "y"
        obj.isCompTurn = True
        obj.board = [["y"], [], ["y"], ["r", "r","y"], ["r"], ["r"], []]
        self.assertEqual(obj.compMove(), 6)

        # detecting position of immediate victory for comp
        obj = Game(True)
        # player whose turn it currently is
        obj.toPlay = "y"
        obj.isCompTurn = True
        obj.board = [["y"], ["r", "y"], ["r","y", "y"], ["r", "r", "y"], [], [], ["r", "r"]]
        self.assertEqual(obj.compMove(), 3)

    def test_addCoinToBoard(self):
        obj = Game(True)
        obj.coinsPlayed = 7
        obj.board = [["y"], [], ["y"], ["r", "r","y"], ["r"], ["r"], []]
        obj.toPlay = "y"
        obj.addCoinToBoard(1)
        self.assertEqual(obj.board, [["y"], ["y"], ["y"], ["r", "r","y"],
                                     ["r"], ["r"], []])
        self.assertEqual(obj.coinsPlayed, 8)

class ButtonManagerTest(unittest.TestCase):

##    def test_init(self):
##        buttonA = Button((0, 0), "buttonaA", lambda x,y: "a")
##        buttonB = Button((40, 40), "buttonaB", lambda x,y: "b")
##        buttonManager = ButtonManager([buttonA, buttonB])
##        self.assertEqual(buttonManager.buttons, [buttonA, buttonB])

    def test_callback(self):

                
        buttonA = Button((0, 0), "buttonA", lambda x,y: 1)
        buttonB = Button((40, 40), "buttonB", lambda x,y: 1)

        def changeA(x,y):
            buttonA.testVar = True
        def changeB(x,y):
            buttonB.testVar = True

        buttonA.callback = changeA
        buttonB.callback = changeB
            
        buttonManager = ButtonManager([buttonA, buttonB])
        buttonA.textX = 50
        buttonB.textX = 50
        buttonManager.callback(1, 1)
        buttonManager.callback(45, 45)
        
        self.assertTrue(buttonA.testVar)
        self.assertTrue(buttonB.testVar)

        buttonA.testVar = False
        buttonManager.callback(-1, -1)
        self.assertFalse(buttonA.testVar)

class ButtonTest(unittest.TestCase):
    def test_init(self):
        button = Button((0,0), "Button", lambda x,y: print("callback"))
        self.assertEqual(button.y, 0)
        self.assertEqual(button.x, 0)
        self.assertEqual(button.textX, 0)
        self.assertEqual(button.text, "Button")
        self.assertFalse(button.clicked)
        self.assertEqual(button.screen, None)

    def test_isWithinBounds(self):
        button = Button((0,0), "Sample Text", lambda x,y: 1)
        button.textX = 40

        self.assertTrue(button.isWithinBounds(20, 20))
        self.assertFalse(button.isWithinBounds(20, 45))
        self.assertFalse(button.isWithinBounds(50, 20))
                         
        

def main():
    unittest.main(verbosity = 3)

main()
