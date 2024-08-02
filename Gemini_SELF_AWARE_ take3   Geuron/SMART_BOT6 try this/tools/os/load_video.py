tool_type_for_TOOL_MANAGER = "all"
load_video_short_description = """Loads a video file from the specified path."""

import cv2
import base64

def load_video(video_path: str) -> dict:
    """Loads a video file from the specified path and returns its base64 encoded data."""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"status": "failure", "message": f"Error opening video file: {video_path}"}

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, frame_encoded = cv2.imencode('.jpg', frame)
            frames.append(frame_encoded)

        cap.release()
        video_data_base64 = base64.b64encode(b''.join(frames)).decode('utf-8')
        return {"status": "success", "video_data": video_data_base64, "video_path": video_path}
    except Exception as e:
        return {"status": "failure", "message": f"Error loading video: {str(e)}"}