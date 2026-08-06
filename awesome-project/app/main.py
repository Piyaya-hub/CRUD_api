from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

app = FastAPI()

tasks = [{"id": 1, "title": "Workout", "done": True},
         {"id": 2, "title": "Study", "done": True},
         {"id": 3, "title": "Walk", "done": False}]

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Title cannot be empty")
        return cleaned_value

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "Successful"}

@app.get("/tasks")
def get_tasks_db():
    return {"database": tasks}

@app.get("/tasks_id/{id}")
def get_task_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    raise HTTPException (
        status_code=404,
        detail=f"Task Id {id} not existing."
    )
    
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    # Determine the next available ID
    next_id = max((t["id"] for t in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": task_data.title,
        "done": False  
    }
    
    tasks.append(new_task)
    return new_task