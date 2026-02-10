# main.py
import cv2
from app.core.config import settings
from app.vision.pose_detector import PoseDetector
# NEW: Import our PushUp logic
from app.exercises.pushup import PushUpCounter 

def main():
    detector = PoseDetector()
    
    # NEW: Initialize the PushUp Counter
    pushup_tracker = PushUpCounter()
    
    cap = cv2.VideoCapture(settings.CAMERA_INDEX)
    cap.set(3, settings.FRAME_WIDTH)
    cap.set(4, settings.FRAME_HEIGHT)
    
    print("Starting Push-Up Tracker. Press 'q' to exit.")

    while True:
        success, img = cap.read()
        if not success:
            continue

        # 1. Find the Pose
        img = detector.find_pose(img)
        
        # 2. Get the list of landmarks
        landmarks = detector.get_landmarks()
        
        # 3. IF we found a person, count their push-ups
        if landmarks:
            # We pass the landmarks to our specific exercise logic
            img = pushup_tracker.process(img, landmarks)

        cv2.imshow("Calisthenics AI - PushUp Tracker", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()