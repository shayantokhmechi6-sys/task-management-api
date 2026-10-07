from app.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    username=Column(String(120), unique=True)
    password_hash=Column(String(250))
    projects=relationship("Project", back_populates="user")
    
class Project(Base):
    __tablename__="projects"
    id=Column(Integer, primary_key=True)
    name=Column(String)
    description=Column(String)
    user_id=Column(Integer , ForeignKey("users.id"))
    user=relationship("User", back_populates="projects")
    tasks=relationship("Task", back_populates="project")

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    description=Column(String)
    status=Column(String)
    priority=Column(String)
    deadline=Column(String)
    project_id=Column(Integer , ForeignKey("projects.id"))
    project=relationship("Project", back_populates="tasks")
   
    
    
    
    