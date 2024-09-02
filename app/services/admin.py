from fastapi import HTTPException
from app.remote.scp import JibriSCP


async def get_video(room_id: str):
    """Get video file from remote server"""
    scp = JibriSCP()

    try:
        scp.get_recording_file(room_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        scp.close_ssh_client()

    return f"/tmp/{room_id}.mp4"
