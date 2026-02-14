from app.utils.geometry import calculate_angle, get_xy
from app.utils.pose_checks import is_body_horizontal, is_back_straight
from app.utils.enums import BodyParts
from app.exercises.exercise import ExerciseCounter


class PushUpCounter(ExerciseCounter):
    position_checks = [
        (is_body_horizontal, "Setup: Lie down horizontally"),
        (is_back_straight, "Setup: Keep your back straight!"),
    ]

    def get_angle(self, landmarks):
        shoulder = get_xy(landmarks[BodyParts.SHOULDER.left])
        elbow = get_xy(landmarks[BodyParts.ELBOW.left])
        wrist = get_xy(landmarks[BodyParts.WRIST.left])
        return calculate_angle(shoulder, elbow, wrist)

    def update_state(self, angle):
        if angle > 160:
            if self.stage == "DOWN":
                self.count += 1
                self.feedback = "Great Rep!"
                print(f"Rep detected! Count: {self.count}")
            self.stage = "UP"

        if angle < 90:
            self.stage = "DOWN"
            self.feedback = "Good Depth"