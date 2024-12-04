import numpy as np
def are_points_near(points, threshold):
    # Convert the list of points to a NumPy array for easier calculations
    points = np.array(points)
    
    # Calculate the pairwise distances
    distances = np.linalg.norm(points[:, np.newaxis] - points[np.newaxis, :], axis=2)
    
    # Find the maximum distance
    max_distance = np.max(distances)
    
    # Check if the maximum distance is less than the threshold
    return max_distance < threshold

def distance(p1,p2):
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def is_near(slope1,slope2,threshold=0.5):
    return abs(slope1-slope2)<threshold