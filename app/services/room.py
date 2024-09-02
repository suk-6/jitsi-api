import jwt
import json
import random
import string
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from app.config import Settings
from app.databases.redis import rd

from app.models.room import RoomModel
from app.databases import session
from app.models.sql.room import RoomParticipantsSQLModel, RoomSQLModel
from app.models.token import JitsiTokenPayload, JitsiTokenUser
from app.models.status import Status

env = Settings()


async def new(user: JitsiTokenUser):
    room: RoomModel = {
        "id": str(uuid4()),
        "name": ''.join(random.choices(string.ascii_uppercase, k=8)),
        "owner": user.model_dump(),
        "participants": [],
        "user_count": 0,
        "status": Status.ACTIVE.value,
    }

    rd.set(f"room:{room['id']}", json.dumps(room))
    return room["id"]


async def join(user: JitsiTokenUser, room_id: str):
    raw_room = rd.get(f"room:{room_id}")
    if not raw_room:
        raise HTTPException(status_code=404, detail="Room not found")

    room: RoomModel = json.loads(rd.get(f"room:{room_id}"))

    token_data: JitsiTokenPayload = {
        "aud": env.jwt_app_id,
        "iss": env.jwt_app_id,
        "sub": f"{env.host}:{env.port}",
        "room": room["name"],
        "room_id": room["id"],
        "exp": datetime.now().timestamp() + 86400,  # 1 day
        "nbf": datetime.now().timestamp(),
        "context": {"user": user.model_dump()},
    }

    token = jwt.encode(token_data, env.jwt_app_secret, algorithm="HS256")

    for p in room["participants"]:
        if p["email"] == user.email:
            return f"{env.front_url}/{room['name']}?token={token}"

    room["participants"].append(user.model_dump())
    room["user_count"] += 1
    rd.set(f"room:{room_id}", json.dumps(room))

    return f"{env.front_url}/{room["name"]}?token={token}"


async def leave(token: str):
    try:
        token_data: JitsiTokenPayload = jwt.decode(token, env.jwt_app_secret, algorithms=["HS256"], audience=env.jwt_app_id)
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    room_id = token_data['room_id']

    room: RoomModel = json.loads(rd.get(f"room:{room_id}"))
    room['user_count'] -= 1
    rd.set(f"room:{room_id}", json.dumps(room))

    if len(room["participants"]) <= 0:
        await terminate(room_id)


async def terminate(room_id: str):
    room: RoomModel = json.loads(rd.get(f"room:{room_id}"))
    room["status"] = Status.TERMINATED.value
    rd.delete(f"room:{room_id}")

    db_room = RoomSQLModel(id=room['id'], name=room['name'], status=room['status'])
    owner = RoomParticipantsSQLModel(room_id=room['id'], email=room['owner']['email'], avatar=room["owner"]['avatar'], name=room["owner"]['name'], isOwner=True)
    participants = [RoomParticipantsSQLModel(room_id=room['id'], email=p['email'], avatar=p['avatar'], name=p['name'], isOwner=False) for p in room['participants']]

    with session:
        session.add(db_room)
        session.add(owner)
        session.add_all(participants)
        session.commit()
