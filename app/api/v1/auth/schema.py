from pydantic import BaseModel


class MagicLoginRequest(BaseModel):
    token: str
