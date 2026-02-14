from app.utils.geometry import calculate_angle, get_xy
from app.utils.pose_checks import is_body_vertical
from app.utils.enums import BodyParts
from app.exercises.exercise import ExerciseCounter


class SquatCounter(ExerciseCounter):
    required_groups = [BodyParts.SHOULDER, BodyParts.HIP, BodyParts.KNEE, BodyParts.ANKLE]
    position_check = staticmethod(is_body_vertical)
    position_feedback = "Setup: Straighten your back!"

    def get_angle(self, landmarks):
        hip = get_xy(landmarks[BodyParts.HIP.left])
        knee = get_xy(landmarks[BodyParts.KNEE.left])
        ankle = get_xy(landmarks[BodyParts.ANKLE.left])
        return calculate_angle(hip, knee, ankle)

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