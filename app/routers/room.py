from fastapi import APIRouter

from app.services.room import new, join, leave

from app.models.token import JitsiTokenUser

router = APIRouter(
    prefix="/room",
    tags=["room"],
)


@router.post("/new")
async def new_room(user: JitsiTokenUser):
    id = await new(user)
    return {"id": id}


@router.post("/join")
async def join_room(user: JitsiTokenUser, room_id: str):
    url = await join(user, room_id)
    return {"url": url}


@router.get("/leave")
async def leave_room(token: str):
    await leave(token)

    return True
