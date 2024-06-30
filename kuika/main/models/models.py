from kuika import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)

    def __init__(self, job_description, requirements) -> None:
        self.job_description = job_description
        self.requirements = requirements
