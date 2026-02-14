from enum import Enum
import mediapipe as mp
from collections import namedtuple

class Workout(Enum):
    PUSHUP = "pushup"
    SQUAT = "squat"
    # PULLUP = "pullup"
    # SITUP = "situp"

_mp = mp.solutions.pose.PoseLandmark
_Pair = namedtuple('BodyPart', ['left', 'right'])

class BodyParts:
    # Face
    EYE = _Pair(left=_mp.LEFT_EYE.value, right=_mp.RIGHT_EYE.value)
    EYE_INNER = _Pair(left=_mp.LEFT_EYE_INNER.value, right=_mp.RIGHT_EYE_INNER.value)
    EYE_OUTER = _Pair(left=_mp.LEFT_EYE_OUTER.value, right=_mp.RIGHT_EYE_OUTER.value)
    EAR = _Pair(left=_mp.LEFT_EAR.value, right=_mp.RIGHT_EAR.value)
    MOUTH = _Pair(left=_mp.MOUTH_LEFT.value, right=_mp.MOUTH_RIGHT.value)

    # Upper Body
    SHOULDER = _Pair(left=_mp.LEFT_SHOULDER.value, right=_mp.RIGHT_SHOULDER.value)
    ELBOW = _Pair(left=_mp.LEFT_ELBOW.value, right=_mp.RIGHT_ELBOW.value)
    WRIST = _Pair(left=_mp.LEFT_WRIST.value, right=_mp.RIGHT_WRIST.value)
    PINKY = _Pair(left=_mp.LEFT_PINKY.value, right=_mp.RIGHT_PINKY.value)
    INDEX = _Pair(left=_mp.LEFT_INDEX.value, right=_mp.RIGHT_INDEX.value)
    THUMB = _Pair(left=_mp.LEFT_THUMB.value, right=_mp.RIGHT_THUMB.value)

    # Lower Body
    HIP = _Pair(left=_mp.LEFT_HIP.value, right=_mp.RIGHT_HIP.value)
    KNEE = _Pair(left=_mp.LEFT_KNEE.value, right=_mp.RIGHT_KNEE.value)
    ANKLE = _Pair(left=_mp.LEFT_ANKLE.value, right=_mp.RIGHT_ANKLE.value)
    HEEL = _Pair(left=_mp.LEFT_HEEL.value, right=_mp.RIGHT_HEEL.value)
    FOOT_INDEX = _Pair(left=_mp.LEFT_FOOT_INDEX.value, right=_mp.RIGHT_FOOT_INDEX.value)

    # Solo landmarks
    NOSE = _mp.NOSE.value