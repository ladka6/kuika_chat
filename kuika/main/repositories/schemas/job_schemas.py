from pydantic import BaseModel, Field
from typing import Optional


class JobCreateSchema(BaseModel):
    job_description: str = Field(..., min_length=1)
    requirements: str


class JobUpdateSchema(BaseModel):
    id: int
    job_description: Optional[str] = Field(None, min_length=1)
    requirements: str
