import unittest
import helper

class TestHelper(unittest.TestCase):

    def setUp(self):
        self.pieces = [(105, 301), (197, 248), (330, 167), (288, 213), (242, 116), (106, 168), (104, 123), (158, 124), (240, 116)]
        self.grid_points = [[43, 86, 129, 172, 215, 258, 301], [44, 88, 132, 176, 220, 264, 308]]  # Replace with your actual y values
        self.expected_results = ['c2', 'e3', 'h5', 'g4', 'f6', 'c5', 'c6', 'd6', 'f6']

    def test_is_in_box(self):
        for i, piece in enumerate(self.pieces):
            location = helper.is_in_box(piece, self.grid_points)
            self.assertEqual(location, self.expected_results[i])

if __name__ == '__main__':
    unittest.main()