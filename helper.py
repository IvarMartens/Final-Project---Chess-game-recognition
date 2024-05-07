import numpy as np
import cv2

def is_square(points):
    # Check if the points form a square
    if len(points) != 4:
        return False

    # Calculate the distance between the points
    d1 = np.sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
    d2 = np.sqrt((points[1][0] - points[2][0])**2 + (points[1][1] - points[2][1])**2)
    d3 = np.sqrt((points[2][0] - points[3][0])**2 + (points[2][1] - points[3][1])**2)
    d4 = np.sqrt((points[3][0] - points[0][0])**2 + (points[3][1] - points[0][1])**2)

    distances = [d1, d2, d3, d4]
    max_distance = max(distances)
    
    for distance in distances:
        if distance < max_distance/3:
            return False
    
    return True

def rotate_image(image, angle):
    # Rotate the image by the given angle (90, 180, 270 degrees)
    if angle == 90:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated_image = cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated_image = image
    return rotated_image

def get_color_at_point(image, x, y):
    # Get the BGR color of the image at a specific point
    return image[y, x]

def adjust_chessboard_orientation(transformed_img, height, width, current_orientation):
    
    # Check the color at bottom-left and bottom-right corners
    bottom_left_color = get_color_at_point(transformed_img, 5, 5)
    bottom_right_color = get_color_at_point(transformed_img, width - 5, 5)
    
    # Determine if the bottom-left is darker than the bottom-right
    if np.mean(bottom_left_color) < np.mean(bottom_right_color):
        # If bottom-left is lighter, rotate 90 degrees
        if current_orientation == 90:
            rotation = 270
        else: 
            rotation = 90
        
        transformed_img = rotate_image(transformed_img, rotation)

    return transformed_img, rotation

def is_in_box(piece_center: tuple, grid_points: list):
    """
    
    @args piece_center: the center of the base of the boinding box of a piece and the grid points (x,y)
    @args grid_points: the intersection points of the chessboard grid in current frame

    returns: the index of the grid point that the piece is in
    """
    x = None
    y = None

    for i in range (7):
        if i == 1:
            if piece_center[0] < grid_points[0][i]:
                x = i
            if piece_center[1] < grid_points[1][i]:
                y = i
        else:
            if piece_center[0] < grid_points[0][i] and piece_center[0] > grid_points[0][i-1]:
                x = i
            if piece_center[1] < grid_points[1][i] and piece_center[1] > grid_points[1][i-1]:
                y = i

        if x != None and y != None:
            return (x,y)

def get_ip(location):
    if location == 'home':
        return 'http://192.168.55.110:8080/video'
    if location == 'uni':
        return 'http://'
    
