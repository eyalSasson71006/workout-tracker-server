import cv2
import numpy as np
from app.utils.geometry import calculate_angle
from app.utils.pose_checks import is_whole_body_in_frame, is_body_vertical

class SquatCounter:
    def __init__(self):
        self.count = 0
        self.stage = "UP"
        self.feedback = "Setup: Get into position"
        
    def process(self, img, landmarks):
        # Check A: Is the user actually on the screen?
        if not is_whole_body_in_frame(landmarks):
            self.feedback = "Frame: Step back / Adjust Camera"
            # Draw simple feedback and return early (Don't count reps!)
            cv2.putText(img, self.feedback, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            return img

        # Check B: Are they in squat position?
        if not is_body_vertical(landmarks):
            self.feedback = "Setup: Straighten your back!"
            cv2.putText(img, self.feedback, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,165,255), 2)
            return img

        # 1. Get Coordinates
        # 27=Ankle, 23=Hip, 25=Knee
        ankle = [landmarks[27].x, landmarks[27].y]
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]

        # 2. Calculate Angle
        angle = calculate_angle(hip, knee, ankle)
        
        # 3. State Machine (The Fixed Logic)
        # Condition: Going Down
        if angle > 160:
            # If we are coming UP from a DOWN position, count the rep FIRST
            if self.stage == "DOWN":
                self.count += 1
                self.feedback = "Great Rep!"
                print(f"Rep detected! Count: {self.count}")
            
            # THEN update the stage to UP
            self.stage = "UP"
            
        if angle < 90:
            self.stage = "DOWN"
            self.feedback = "Good Depth"

        # 4. Draw Feedback on Screen
        # Status Box
        cv2.rectangle(img, (0,0), (350,80), (245,117,16), -1)
        
        # Rep Count
        cv2.putText(img, str(self.count), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage (UP/DOWN)
        cv2.putText(img, self.stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255,255,255), 2, cv2.LINE_AA)
        
        # Optional: Display the Angle for debugging
        cv2.putText(img, str(int(angle)), 
                           (200, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255, 255, 255), 2, cv2.LINE_AA)
            
        return img