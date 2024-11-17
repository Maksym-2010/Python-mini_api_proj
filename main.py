from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database.base import create_db, session
from database.todo import ToDo

create_db()
app = FastAPI()


@app.get("/tasks/")
async def get_tasks():
    return session.query(ToDo).all()



@app.get("/tasks/{id}")
async def get_task(id: int):
    task = session.query(ToDo).get(id)
    return task



@app.post("/tasks/")
async def create_task(title: str, description: str):
    task = ToDo(title=title, description=description)
    session.add(task)
    session.commit()
    return {"message": "Task is Created"}



@app.put("/tasks/{id}/")
async def update_task(id: int, title: str = None, description: str = None):
    if not title and not description:
        return Response(content="Fill description or title to update", status_code=404)
    task = session.query(ToDo).get(id)
    if title:
        task.title = title
    if description:
        task.description = description
    return {"message": f"{task.title} has been updated"}



@app.delete("/tasks/{id}/")
async def delete_task(id: int):
    task = session.query(ToDo).get(id)
    session.delete(task)
    session.commit()
    return {"message": "Task is deleted"}



@app.patch("/tasks/{id}/complete/")
async def complete_task(id: int):
    task = session.query(ToDo).get(id)
    task.completed = True
    session.commit()
    return {"message": f"Task {task.title} is Completed"}



@app.patch("/tasks/{id}/uncomplete/")
async def uncomplete_task(id: int):
    task = session.query(ToDo).get(id)
    task.completed = False
    session.commit()
    return {"message": f"Task {task.title} is UnCompleted"}



@app.get("/tasks/completed/")
async def completed_tasks():
    completed = session.query(ToDo).filter(ToDo.completed == True).all()
    return completed


@app.get("/tasks/not_completed/")
async def not_completed_tasks():
    not_completed = session.query(ToDo).filter(ToDo.completed == False).all()
    return not_completed
        

cas = {
    "id": 1, 
    "isAvaileble": True
}