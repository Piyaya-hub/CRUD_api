from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI()

# Acting database for tasks lists
# Data were added using swagger for testing of each functions.

Prototype_tasks = [ 
    {"id": 1, "title": "Part 1", "done": False},
    {"id": 2, "title": "Part 2", "done": False},
    {"id": 3, "title": "Part 3", "done": False}
    ]

tasks = list(Prototype_tasks)

# A pydantic model for input validation during task creation, POST endpoint specifically.
class TaskCreate(BaseModel):
    title: str
    
    # a field validator for specific fields with specific  validation steps.
    @field_validator("title")
    @classmethod
    def input_title_validation(cls, value: str) -> str:
        stripped_title = value.strip()
        if not stripped_title:
            raise ValueError("Title cannot be empty")
        return stripped_title    
    
class TaskUpdate(BaseModel):
    title:Optional[str] = None
    done: Optional[bool] = None
    
    # a field validator for specific fields with specific  validation steps.
    @field_validator("title")
    @classmethod
    def change_validation(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped_title = value.strip()
        if not stripped_title:
            raise ValueError("Title cannot be empty")
        return stripped_title
    
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/health")
# def health():
#     return {"status": "Successful"}

# Endpoint for tasks creation integrated with pydantic validation
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task_input: TaskCreate):
    next_id = max((i["id"] for i in tasks), default=0) + 1
    
    new_task = {
         "id": next_id,
         "title": task_input.title,
         "done": False
     }
     
    tasks.append(new_task)
    return new_task

@app.post("/reset")
def reset_task():
    global tasks
    
    tasks = [task.copy() for task in Prototype_tasks]
    
    return {
        "message": "Database had been reset for testing.",
        "tasks": tasks
        }
        

#Endpoint created for get tasks
@app.get("/list_of_tasks")
def get_tasks_db():
    return {"database": tasks}

#Endpoint for displaying list of task with constraints
@app.get("/tasks")
def get_tasks_status(done: Optional[bool] = None):    
    if done is not None:
        return [task for task in tasks if task["done"] == done]
    return tasks

#Endpoint for searching tasks using String
@app.get("/tasks_search")
def get_search_tasks(search: Optional[str] = None):
    if search is not None:
        return [task for task in tasks if search.lower().strip() in task["title"].lower()]
    return tasks

#Endpoint finding specific tasks using unique Ids
@app.get("/tasks/{id}")
def get_task_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    raise HTTPException (
        status_code=404,
        detail=f"Task Id {id} not existing." #
    )

# Endpoint for summary of the entire task program
@app.get("/tasks_status")
def get_tasks_status():
    finished_count = 0
    
    Total_task = len(tasks)
    
    for task in tasks:
        if task["done"] == True:
            finished_count += 1
    
    return {
        "total": Total_task,
        "Finished": finished_count,
        "Unfinished": Total_task - finished_count
        }
    
# Endpoint for tasks updates integrated with pydantic validation
@app.put("/tasks/{id}")
async def update_task(id: int, task_update: TaskUpdate):
    
    for task in tasks:
        if task["id"] == id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
        
    raise HTTPException(
        status_code =  status.HTTP_404_NOT_FOUND, 
        detail= f"Id number {id} not found."
        )

# Endpoint for task deletion using enumerate(tasks) for field's pairing
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return status.HTTP_204_NO_CONTENT
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= f"Id {id} not found"
        )
        