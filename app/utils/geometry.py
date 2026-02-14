import numpy as np

def get_xy(landmark):
    """Extracts [x, y] from a MediaPipe landmark."""
    return [landmark.x, landmark.y]

def calculate_angle(a, b, c):
    """
    Calculates the angle at point 'b' given three points [x, y].
    a, b, c are typically MediaPipe landmarks.
    """
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle