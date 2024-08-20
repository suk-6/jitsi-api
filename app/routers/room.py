from fastapi import APIRouter

router = APIRouter(
    prefix="/room",
    tags=["room"],
)


@router.get("/new")
async def new_room():
    return {"message": "New Room"}
