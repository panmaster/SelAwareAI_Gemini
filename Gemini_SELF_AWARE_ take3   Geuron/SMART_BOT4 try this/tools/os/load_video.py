tool_type_for_TOOL_MANAGER = "all"
load_video_short_description=  """Loads a video file from the specified path."""
# You might need to install moviepy: pip install moviepy
import moviepy.editor as mpe

def load_video(video_path: str) -> dict:
    """Loads a video file from the specified path."""
    try:
        video = mpe.VideoFileClip(video_path)
        # ... (Optional: Extract frames, get metadata, etc.)
        return {"status": "success", "video_object": video, "video_path": video_path}
    except Exception as e:
        return {"status": "failure", "message": f"Error loading video: {str(e)}"}