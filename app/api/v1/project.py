from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.models.project import Job, Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate, db: AsyncSession = Depends(get_db)
):
    db_project = Project(name=project_data.name)

    if project_data.jobs:
        for job in project_data.jobs:
            db_project.jobs.append(Job(status=job.status))

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project, attribute_names=["jobs"])

    return db_project


@router.get("", response_model=List[ProjectResponse])
async def get_projects(db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload

    stmt = select(Project).options(selectinload(Project.jobs))

    result = await db.execute(stmt)
    projects = result.scalars().all()

    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload

    stmt = (
        select(Project)
        .where(Project.id == project_id)
        .options(selectinload(Project.jobs))
    )
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return project
