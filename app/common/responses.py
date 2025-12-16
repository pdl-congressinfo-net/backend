from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class MessageResponse(BaseModel):
    message: str


class ApiResponse(GenericModel, Generic[T]):
    data: T
    meta: dict | None = None
