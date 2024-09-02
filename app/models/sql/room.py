from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class RoomSQLModel(SQLModel, table=True):
    __tablename__ = "room"
    id: str = Field(primary_key=True)
    name: str
    status: int

    participants: List["RoomParticipantsSQLModel"] = Relationship(
        back_populates="room"
    )


class RoomParticipantsSQLModel(SQLModel, table=True):
    __tablename__ = "participants"
    id: Optional[int] = Field(primary_key=True, default=None)
    email: str
    isOwner: bool

    room_id: str = Field(foreign_key="room.id")
    room: Optional[RoomSQLModel] = Relationship(back_populates="participants")
