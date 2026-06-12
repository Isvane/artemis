from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    status: Optional[str] = "PENDING"


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    jobs: Optional[List[JobCreate]] = []


class ProjectResponse(ProjectBase):
    id: int
    jobs: List[JobResponse] = []

    model_config = ConfigDict(from_attributes=True)
