from fastapi import Depends, FastAPI

from .dependencies import check_request_server
from .routers import room

app = FastAPI(dependencies=[Depends(check_request_server)])

app.include_router(room)


@app.get("/")
async def root():
    return {"message": "Jitsi API Server"}
