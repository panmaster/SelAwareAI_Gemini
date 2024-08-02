tool_type_for_TOOL_MANAGER = "all"
load_audio_short_description= """Loads an audio file from the specified path."""



# You might need to install pydub: pip install pydub
from pydub import AudioSegment

def load_audio(audio_path: str) -> dict:
    """Loads an audio file from the specified path."""
    try:
        audio = AudioSegment.from_file(audio_path)
        audio_bytes = audio.raw_data  # Get raw audio bytes
        return {"status": "success", "audio_data": audio_bytes, "audio_path": audio_path}
    except Exception as e:
        return {"status": "failure", "message": f"Error loading audio: {str(e)}"}