import cv2
from abc import ABC, abstractmethod
from app.utils.pose_checks import is_whole_body_in_frame


class ExerciseCounter(ABC):
    """
    Base class for all exercise counters.
    Subclasses configure themselves via class-level properties
    and override get_angle() and update_state() for their specific logic.
    """

    # --- Subclass configuration (override as needed) ---
    required_groups = None          # BodyParts needed in frame (None = default)
    position_checks = []            # List of (check_fn, feedback_msg) tuples

    def __init__(self):
        self.count = 0
        self.stage = None
        self.feedback = "Setup: Get into position"

    @abstractmethod
    def get_angle(self, landmarks):
        """Return the angle to track. Each exercise picks its own joints."""
        pass

    @abstractmethod
    def update_state(self, angle):
        """Update stage/count/feedback based on the angle."""
        pass

    def process(self, img, landmarks):
        # Check A: Is the user actually on the screen?
        if not is_whole_body_in_frame(landmarks, self.required_groups):
            self.feedback = "Frame: Step back / Adjust Camera"
            cv2.putText(img, self.feedback, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            return img

        # Check B: Run all position checks (stops on first failure)
        for check_fn, feedback_msg in self.position_checks:
            if not check_fn(landmarks):
                self.feedback = feedback_msg
                cv2.putText(img, self.feedback, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,165,255), 2)
                return img

        # 1. Get angle from subclass
        angle = self.get_angle(landmarks)

        # 2. Let subclass update its state machine
        self.update_state(angle)

        # 3. Draw HUD
        self._draw_hud(img, angle)

        return img

    def _draw_hud(self, img, angle):
        """Draws the status box with rep count, stage, and angle."""
        # Status Box
        cv2.rectangle(img, (0,0), (350,80), (245,117,16), -1)

        # Rep Count
        cv2.putText(img, str(self.count),
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255,255,255), 2, cv2.LINE_AA)

        # Stage
        cv2.putText(img, self.stage or "",
                    (60,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255,255,255), 2, cv2.LINE_AA)

        # Angle (debug)
        cv2.putText(img, str(int(angle)),
                    (200, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)