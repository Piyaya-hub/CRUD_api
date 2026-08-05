from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [{"id": 1, "title": "Workout", "done": True},
         {"id": 2, "title": "Study", "done": True},
         {"id": 3, "title": "Walk", "done": False}]


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
        
    