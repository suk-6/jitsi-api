from fastapi import APIRouter

router = APIRouter(
    prefix="/room",
    tags=["room"],
)


@router.get("/new")
async def new_room():
    return {"message": "New Room"}


@router.get("/join")
async def join_room():
    return {"message": "Join Room"}


@router.get("/leave")
async def leave_room():
    return {"message": "Leave Room"}


@router.get("/terminate")
async def terminate_room():
    return {"message": "Terminate Room"}
