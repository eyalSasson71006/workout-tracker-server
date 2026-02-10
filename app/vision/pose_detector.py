import cv2
import mediapipe as mp
from app.core.config import settings

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize the Pose model once
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=settings.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=settings.MIN_TRACKING_CONFIDENCE,
            model_complexity=settings.MODEL_COMPLEXITY
        )
        
    def find_pose(self, img, draw=True):
        """Processes the image and finds the pose."""
        # Convert to RGB (MediaPipe requirement)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process
        self.results = self.pose.process(img_rgb)
        
        # Draw skeleton on the image
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(
                img, 
                self.results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )
        return img
    
    def get_landmarks(self):
        """Returns the raw landmarks list if found."""
        if self.results.pose_landmarks:
            return self.results.pose_landmarks.landmark
        return None

    def is_whole_person_detected(self):
        """Returns True if a whole person is detected."""
        if self.results.pose_landmarks:
            return True
        return False