from pydantic import BaseModel
from typing import List


class StartChatResponse(BaseModel):
    requirements: List[str]
    job_description: str
    current_step: int


class ChatInput(BaseModel):
    requirements: List[str]
    job_description: str
    current_step: int
    message: str
