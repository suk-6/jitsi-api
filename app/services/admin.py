import json
from fastapi import HTTPException

from sqlmodel import select

from app.databases import rd, session
from app.models.room import RoomModel
from app.models.sql.room import RoomParticipantsSQLModel, RoomSQLModel
from app.remote.scp import JibriSCP


async def get_rooms():
    """Get all rooms"""
    rooms: list[RoomModel] = []

    # Redis Rooms (Active)
    redis_keys = rd.keys(pattern="room:*")

    for key in redis_keys:
        room = json.loads(rd.get(key))

        rooms.append(
            {
                "id": room["id"],
                "name": room["name"],
                "owner": {
                    "avatar": room["owner"]["avatar"],
                    "email": room["owner"]["email"],
                    "name": room["owner"]["name"],
                },
                "participants": [
                    {
                        "avatar": p["avatar"],
                        "email": p["email"],
                        "name": p["name"],
                    }
                    for p in room["participants"]
                ],
                "status": room["status"],
            }
        )

    # DB Rooms (Terminated)
    with session:
        statement = select(RoomSQLModel)
        raw_rooms = session.exec(statement).all()

    for room in raw_rooms:
        with session:
            owner = session.exec(
                select(RoomParticipantsSQLModel).where(
                    RoomParticipantsSQLModel.isOwner == True
                )
            ).one()
            participants = session.exec(
                select(RoomParticipantsSQLModel).where(
                    RoomParticipantsSQLModel.isOwner == False
                )
            ).all()

        rooms.append(
            {
                "id": room.id,
                "name": room.name,
                "owner": {
                    "avatar": owner.avatar,
                    "email": owner.email,
                    "name": owner.name,
                },
                "participants": [
                    {
                        "avatar": p.avatar,
                        "email": p.email,
                        "name": p.name,
                    }
                    for p in participants
                ],
                "status": room.status,
            }
        )

    return rooms


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
