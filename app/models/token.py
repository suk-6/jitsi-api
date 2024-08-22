from pydantic import BaseModel


class JitsiTokenUser(BaseModel):
    avatar: str  # URL
    name: str
    email: str


class JitsiTokenContext(BaseModel):
    user: JitsiTokenUser


class JitsiTokenPayload(BaseModel):
    aud: str  # Application ID
    iss: str  # Issuer
    sub: str  # Subject (Public Host)
    room: str  # Room Name
    exp: int  # Expiration Time
    nbf: int  # Not Before Time
    context: JitsiTokenContext
