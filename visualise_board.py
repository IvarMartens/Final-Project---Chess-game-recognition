import chess
import numpy as np
from fentoimage.board import BoardImage
import cv2

def visualise_board(fen):
    renderer = BoardImage(fen)
    image = renderer.render()
    # Convert the PIL image to a NumPy array
    image_np = np.array(image)

    image_np = cv2.resize(image_np, (640, 640), interpolation = cv2.INTER_AREA)
    
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    return image_bgr