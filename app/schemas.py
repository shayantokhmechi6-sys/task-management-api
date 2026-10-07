from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str 
    model_config = ConfigDict(from_attributes=True)
    
class LoginCreate(BaseModel):
    username:str
    password:str

class LoginResponse(BaseModel):
    access_token:str
    token_type:str

class ProjectCreate(BaseModel):
    name:str
    description:str

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str
    description:str
    user_id:int
    
class TaskCreate(BaseModel):
    name:str
    description:str
    status:str
    priority:str
    deadline:str

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str
    description:str
    status:str
    priority:str
    deadline:str
    
    
    