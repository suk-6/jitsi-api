from pydantic import BaseModel

from app.models.token import JitsiTokenUser


class RoomModel(BaseModel):
    id: str
    name: str
    owner: JitsiTokenUser
    participants: list[JitsiTokenUser]
    status: int
