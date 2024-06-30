from kuika.main.models.models import Job
from kuika import db
from kuika.main.repositories.schemas.job_schemas import JobCreateSchema
from pydantic import ValidationError


class JobRepository:
    @staticmethod
    def create_job(job_description, requirements) -> Job:
        try:
            validated = JobCreateSchema(
                job_description=job_description, requirements=requirements
            )
        except ValidationError as e:
            raise e
        job = Job(
            job_description=validated.job_description,
            requirements=validated.requirements,
        )
        db.session.add(job)
        db.session.commit()
        return job

    @staticmethod
    def find_requirements(job_description) -> str:
        job: Job = Job.query.filter_by(job_description=job_description).first()
        return job.requirements

    @staticmethod
    def list_jobs():
        jobs = Job.query.with_entities(Job.job_description).all()
        jobs = [item[0] for item in jobs]
        return jobs
