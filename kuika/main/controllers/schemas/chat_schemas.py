from pydantic import BaseModel
from typing import List


class StartChatDTO(BaseModel):
    job_description: str


class ChatDTO(BaseModel):
    requirements: List[str]
    job_description: str
    current_step: int
    message: str


class UserQueryDTO(BaseModel):
    query: str
