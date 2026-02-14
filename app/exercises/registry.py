from app.exercises.squat import SquatCounter
from app.exercises.pushup import PushUpCounter
from app.utils.enums import Workout

WORKOUT_REGISTRY = {
    Workout.PUSHUP: PushUpCounter,
    Workout.SQUAT: SquatCounter,
    # Workout.PULLUP: PullUpCounter,
    # Workout.SITUP: SitUpCounter
}
