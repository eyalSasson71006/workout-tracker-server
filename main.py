# main.py
import cv2
from app.core.config import settings
from app.utils.enums import Workout
from app.vision.pose_detector import PoseDetector
from app.exercises.registry import WORKOUT_REGISTRY

def main():
    detector = PoseDetector()

    cap = cv2.VideoCapture(settings.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.FRAME_HEIGHT)
    
    workout_names = [w.value.capitalize() for w in Workout]
    print("Starting Workout Tracker. Press 'q' to exit.")

    selected_workout = None
    while selected_workout is None:
        user_input = input(f"Please select a workout from the following list: {workout_names}\n").strip().lower()
        try:
            selected_workout = Workout(user_input)
        except ValueError:
            print("Invalid selection, try again.")

    # Initialize the selected workout tracker
    workout_tracker = WORKOUT_REGISTRY[selected_workout]()

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
            img = workout_tracker.process(img, landmarks)

        cv2.imshow(f"Calisthenics AI - {selected_workout.value.capitalize()} Tracker", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()