from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import TaskCreate,TaskResponse
from app.models import User,Project,Task
from app.dependencies import get_current_user,get_db
from logging_config import logger

router=APIRouter()

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
def create_task(project_id:int,task:TaskCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_get_project=db.query(Project).filter(Project.id==project_id).first()
    if not db_get_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not db_get_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    new_task=Task(
        name=task.name,
        description=task.description,
        status=task.status,
        priority=task.priority,
        deadline=task.deadline,
        project_id=project_id
    )
    db.add(new_task)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while creating task:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    db.refresh(new_task)
    logger.info("Task created successfully")
    return new_task

@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
def get_tasks(project_id:int,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_project=db.query(Project).filter(Project.id==project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not db_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    db_get_tasks=db.query(Task).filter(Task.project_id==project_id).all()
    return db_get_tasks
    
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def tasks(task_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_task=db.query(Task).filter(Task.id==task_id).first()
    if not db_task:
        raise HTTPException(status_code=404 , detail="Task not found")
    db_task_project=db.query(Project).filter(Project.id==db_task.project_id).first()
    if not db_task_project:
        raise HTTPException(status_code=404 , detail="Project not found")
    if not db_task_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id:int, task:TaskCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_update_task=db.query(Task).filter(Task.id==task_id).first()
    if not db_update_task:
        raise HTTPException(status_code=404 , detail="Task not found")
    db_get_task_project=db.query(Project).filter(Project.id==db_update_task.project_id).first()
    if not db_get_task_project:
        raise HTTPException(status_code=404 , detail="Project not found")
    if not db_get_task_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    db_update_task.name=task.name
    db_update_task.description=task.description
    db_update_task.status=task.status
    db_update_task.priority=task.priority
    db_update_task.deadline=task.deadline
    try:
       db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while updating task:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    db.refresh(db_update_task)
    logger.info("Task updated successfully")
    return db_update_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id:int,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_delete_task=db.query(Task).filter(Task.id==task_id).first()
    if not db_delete_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_project=db.query(Project).filter(Project.id==db_delete_task.project_id).first()
    if not db_project:
        raise HTTPException(status_code=404 , detail="Project not found")
    if not db_project.user_id==current_user.id:
        logger.warning("Unauthorized project access attempt")
        raise HTTPException(status_code=403 , detail="User cannot access")
    db.delete(db_delete_task)
    try:
       db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while deleting task:{e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.info("Task deleted successfully")
    return{
        "message":"Task deleted successfully"
    }
    
    
    
