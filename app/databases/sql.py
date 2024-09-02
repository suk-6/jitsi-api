from sqlmodel import SQLModel, create_engine, Session

from app.config import Settings

from app.models.sql.room import *

env = Settings()

engine = create_engine(
    f"postgresql://{env.postgres_user}:{env.postgres_password}@{env.postgres_host}:{env.postgres_port}/{env.postgres_db}"
)

SQLModel.metadata.create_all(engine)

session = Session(engine)
