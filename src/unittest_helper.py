import unittest
import helper

class TestHelper(unittest.TestCase):

    def setUp(self):
        self.pieces = [(105, 301), (197, 248), (330, 167), (288, 213), (242, 116), (106, 168), (104, 123), (158, 124), (240, 116)]
        self.grid_points = [[43, 86, 129, 172, 215, 258, 301], [44, 88, 132, 176, 220, 264, 308]]  # Replace with your actual y values
        self.expected_results = ['c2', 'e3', 'h5', 'g4', 'f6', 'c5', 'c6', 'd6', 'f6']

    def test_is_in_box(self):
        for i, piece in enumerate(self.pieces):
            location = helper.is_in_location(piece, self.grid_points, 344, 352)
            self.assertEqual(location, self.expected_results[i])

class TestIsLegalMove(unittest.TestCase):
    def test_empty_old_fen(self):
        new_fen = "8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1"
        self.assertEqual(helper.is_legal_move('', new_fen), helper.check_first_state(new_fen))

    def test_same_fen(self):
        fen = "8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1"
        self.assertEqual(helper.is_legal_move(fen, fen), True)

    def test_legal_move(self):
        old_fen = "8/5k2/2qr2p1/5p2/2PP4/8/2Q2K2/6R1 w - - 0 1"
        new_fen = "8/5k2/2qr2p1/2P2p2/3P4/8/2Q2K2/6R1 w - - 0 1"
        self.assertEqual(helper.is_legal_move(old_fen, new_fen), True)

    def test_illegal_move(self):
        old_fen = "8/5k2/2qr2p1/5p2/2PP4/8/2Q2K2/6R1 w - - 0 1"
        new_fen = "8/5k2/2qr2p1/5p2/3P4/2P5/2Q2K2/6R1 b - - 0 1"
        self.assertEqual(helper.is_legal_move(old_fen, new_fen), False)

    def test_valid_first_state(self):
        old_fen = ''
        valid_fen = "8/5k2/2qr2p1/5p2/2PP4/8/2Q2K2/6R1 w - - 0 1"
        self.assertEqual(helper.is_legal_move(old_fen, valid_fen), True)

    def test_invalid_first_state(self):
        old_fen = ''
        invalid_fen = "8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.assertEqual(helper.is_legal_move(old_fen, invalid_fen), False)

if __name__ == '__main__':
    unittest.main()