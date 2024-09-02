from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import check_request_server
from .config import Settings
from .routers import room

app = FastAPI(dependencies=[Depends(check_request_server)])
env = Settings()

origins = [
    env.front_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(room)
