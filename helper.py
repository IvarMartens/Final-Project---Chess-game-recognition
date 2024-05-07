import numpy as np

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

def get_ip(location):
    if location == 'home':
        return 'http://192.168.55.110:8080/video'
    if location == 'uni':
        return 'http://'