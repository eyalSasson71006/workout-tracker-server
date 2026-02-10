
class Settings:
    # Camera Settings
    CAMERA_INDEX = 0
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720
    
    # AI/MediaPipe Settings
    MIN_DETECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.5
    MODEL_COMPLEXITY = 1  # 0=Lite, 1=Full, 2=Heavy (more accurate, slower)

settings = Settings()