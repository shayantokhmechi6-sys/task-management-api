from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProjectCreate,ProjectResponse
from app.dependencies import get_db,get_current_user
from app.models import User,Project
from logging_config import logger
router=APIRouter()

@router.post("/projects",response_model=ProjectResponse)
def projects(project:ProjectCreate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    new_project=Project(
        name=project.name,
        description=project.description,
        user_id=current_user.id
    )
    db.add(new_project)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while creating project:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    db.refresh(new_project)
    logger.info("Project created successfully")
    return new_project

@router.get("/projects" , response_model=list[ProjectResponse])
def get_projects(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_get_projects=db.query(Project).filter(Project.user_id==current_user.id).all()
    return db_get_projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id:int , current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_project=db.query(Project).filter(Project.id==project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not db_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    return db_project
        
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project:ProjectCreate,project_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_update_project=db.query(Project).filter(Project.id==project_id).first()
    if not db_update_project:
        raise HTTPException(status_code=404 , detail="Project not found")
    if not db_update_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    db_update_project.name=project.name
    db_update_project.description=project.description
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while updating project:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    db.refresh(db_update_project)
    logger.info("Project updated successfully")
    return db_update_project
        
@router.delete("/projects/{project_id}")
def delete_project(project_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_delete_project=db.query(Project).filter(Project.id==project_id).first()
    if not db_delete_project:
        raise HTTPException(status_code=404 , detail="Project not found")
    if not db_delete_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    db.delete(db_delete_project)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while deleting project:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Project deleted successfully")
    return{
        "message":"Project deleted successfully"
    }
    
    