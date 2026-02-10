import mediapipe as mp

def _is_point_visible(point, visibility_threshold):
    """Returns True if a single landmark is visible and within screen bounds."""
    if point.visibility < visibility_threshold:
        return False
    # Small buffer (-0.05 to 1.05) to be lenient if a limb slightly clips the edge
    if not (-0.05 <= point.x <= 1.05 and -0.05 <= point.y <= 1.05):
        return False
    return True

def is_whole_body_in_frame(landmarks, required_groups=None, visibility_threshold=0.5):
    """
    Checks if the body is visible in the frame.
    For paired body parts (left/right), at least ONE side must be visible.
    
    Args:
        landmarks: The list of pose landmarks.
        required_groups: List of landmark groups to check. Each group is either
                         a single index or a tuple of (left, right) indices.
        visibility_threshold: Minimum confidence score (0.0 to 1.0).
    """
    if not landmarks:
        return False
        
    mp_pose = mp.solutions.pose
    # Default: check key points, where left/right pairs need only one side visible
    if required_groups is None:
        required_groups = [
            mp_pose.PoseLandmark.NOSE.value,                                                    # solo
            (mp_pose.PoseLandmark.LEFT_WRIST.value, mp_pose.PoseLandmark.RIGHT_WRIST.value),
            (mp_pose.PoseLandmark.LEFT_ANKLE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value),
            (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.RIGHT_HIP.value),    
        ]

    for group in required_groups:
        if isinstance(group, tuple):
            # Paired landmark: at least one side must be visible
            if not any(_is_point_visible(landmarks[idx], visibility_threshold) for idx in group):
                return False
        else:
            # Solo landmark: must be visible
            if not _is_point_visible(landmarks[group], visibility_threshold):
                return False
            
    return True

def is_body_horizontal(landmarks):
    """
    Checks if the torso is roughly horizontal (Parallel to the ground).
    Compares the Y-coordinate (height) of Shoulders vs Hips.
    """
    mp_pose = mp.solutions.pose
    
    # Get Key Points
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    # Use the more visible side for each body part
    shoulder = left_shoulder if left_shoulder.visibility > right_shoulder.visibility else right_shoulder
    hip = left_hip if left_hip.visibility > right_hip.visibility else right_hip

    # Calculate vertical distance (Y-axis difference)
    # If Y difference is small, the body is flat.
    # If Y difference is large, the body is upright.
    diff = abs(shoulder.y - hip.y)
    
    # Threshold: 0.15 is roughly 15% of the screen height.
    # If shoulder and hip are within 15% height of each other -> Horizontal.
    return diff < 0.15