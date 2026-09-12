from pydantic import BaseModel, ConfigDict, EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class JWTPayloadSchema(BaseModel):
    sub: str
    role: str
    iat: int
    exp: int

    model_config = ConfigDict(from_attributes=True)