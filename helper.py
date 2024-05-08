import numpy as np
import cv2

def is_square(points):  
    # order points on x values
    points = sorted(points, key=lambda x: x[0])

    good_points = []
    for i in range(len(points)):
        if i + 1 > len(points) - 1:
            j = 0
        else:
            j = i + 1
        
        # Calculate the distance between two points
        distance = np.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
        if distance > 100:
            good_points.append(points[i])
 
    
    if len(good_points) == 4:
        #calculate the distance to all the other good_points
        distances = []
        for i in range(len(good_points)):
            for j in range(len(good_points)):
                if i != j:
                    distance = np.sqrt((good_points[i][0] - good_points[j][0])**2 + (good_points[i][1] - good_points[j][1])**2)
                    distances.append(distance)
        
        if min(distances) < 50:
            is_square = False
        else:
            is_square = True
    else:
        is_square = False

    return is_square, good_points
        
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

def adjust_chessboard_orientation(transformed_img, height, width):
    
    # Check the color at bottom-left and bottom-right corners
    bottom_left_color = get_color_at_point(transformed_img, 5, 5)
    bottom_right_color = get_color_at_point(transformed_img, width - 5, 5)
    
    # Determine if the bottom-left is darker than the bottom-right
    if np.mean(bottom_left_color) < np.mean(bottom_right_color):
         transformed_img = rotate_image(transformed_img, 90)

    return transformed_img

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
    
