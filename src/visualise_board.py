import chess
import numpy as np
from fentoimage.board import BoardImage
import cv2
import helper


def visualise_board(fen, move):
    renderer = BoardImage(fen)
    if move == None:
        image = renderer.render()
    else:
        # split move string into start and end squares. 2 charecters each
        move = str(move)
        start = move[:2]
        end = move[2:]
        image = renderer.render(highlighted_squares=(chess.parse_square(start), chess.parse_square(end)))

    # Convert the PIL image to a NumPy array
    image_np = np.array(image)

    image_np = cv2.resize(image_np, (640, 640), interpolation = cv2.INTER_AREA)
    
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    return image_bgr