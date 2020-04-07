''' CS5001-Project
    test_game.py
    Akash Kulkarni

    Tests most functions in game.py that exclusively deal with the functionality
    of the game as opposed to graphics.
'''

from game import Game
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
     

def main():
    unittest.main(verbosity = 3)

main()
