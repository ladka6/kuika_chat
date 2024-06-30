from kuika.main.utils.llm import LLMInteraction
from flask import session
from kuika.main.repositories.job_repository import JobRepository
from kuika.main.services.schemas.chat_service_schemas import (
    StartChatResponse,
    ChatInput,
)
from typing import Any, Dict


class ChatService:
    def __init__(self) -> None:
        self.job_repository = JobRepository()
        self.llm_interaction = LLMInteraction()

    def start_chat(self, job_description: str) -> Dict[str, Any]:
        session_id = str(session["config_id"])

        summarized_job_description = self.summarize_job_description(job_description)
        all_jobs = self.job_repository.list_jobs()

        if summarized_job_description in all_jobs:
            res = self.job_repository.find_requirements(summarized_job_description)

        else:  # if job already exists
            res = self.llm_interaction.get_requirements(
                job_description, session_id=session_id
            )

            self.job_repository.create_job(summarized_job_description, res)

        res_split = [line.strip() for line in res.strip().split("\n") if line.strip()][
            1:
        ]
        response = StartChatResponse(
            requirements=res_split,
            job_description=job_description,
            current_step=0,
        )

        return response.model_dump(mode="json")

    def summarize_job_description(self, job_description: str) -> str:
        res = self.llm_interaction.summarize_job_description(job_description)
        return res

    async def find_requirements(self, job_description: str) -> str:
        return ""

    def chat(self, input: ChatInput) -> str:
        job_description = input.job_description
        requirements = input.requirements
        current_step = input.current_step
        message = input.message
        completed_steps = len(requirements) - current_step
        res = self.llm_interaction.chat(
            requirements=requirements,
            job_description=job_description,
            current_step=current_step,
            completed_steps=completed_steps,
            message=message,
        )
        return res
