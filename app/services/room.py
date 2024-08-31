import json
from uuid import uuid4

from app.databases.redis import rd

from app.models.token import JitsiTokenUser
from app.models.status import Status


async def new(user: JitsiTokenUser):
    room = {
        "id": str(uuid4()),
        "owner": user.model_dump(),
        "status": Status.ACTIVE.value,
    }

    await rd.set(f"room:{room['id']}", json.dumps(room))
    return room
