import jwt
import json
import random
import string
from datetime import datetime
from uuid import uuid4

from app.config import Settings
from app.databases.redis import rd

from app.models.room import RoomModel
from app.models.token import JitsiTokenPayload, JitsiTokenUser
from app.models.status import Status

env = Settings()


async def new(user: JitsiTokenUser):
    room: RoomModel = {
        "id": str(uuid4()),
        "name": ''.join(random.choices(string.ascii_uppercase, k=8)),
        "owner": user.model_dump(),
        "participants": [],
        "status": Status.ACTIVE.value,
    }

    rd.set(f"room:{room['id']}", json.dumps(room))
    return room["id"]


async def join(user: JitsiTokenUser, room_id: str):
    room: RoomModel = json.loads(rd.get(f"room:{room_id}"))
    room["participants"].append(user.model_dump())
    rd.set(f"room:{room_id}", json.dumps(room))

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

    return f"{env.front_url}/{room["name"]}?token={token}"
