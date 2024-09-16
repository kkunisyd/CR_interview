from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

def get_students(file):
    with open(file) as f:
        return f.readlines()
    
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

indexes = {}
students = {}
colours = ["red", "pink", "green", "blue", "orange", "yellow", "white"]
for colour in colours:

    students[colour] = get_students(f"{colour}.txt")
    indexes[colour] = 0

templates = Jinja2Templates(directory=".")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("code_review.html", {"request": request})


@app.get("/{color}/now", response_class=PlainTextResponse)
def get_current(color:str):
    current = indexes[color]
    if len(students[color]) <= current:
        return "N/A"
    return students[color][current].strip().replace("\t", " ")

@app.get("/{color}/next", response_class=PlainTextResponse)
def get_next(color:str):
    next = indexes[color] + 1
    if len(students[color]) <= next:
        return "N/A"
    return students[color][next].strip().replace("\t", " ")

@app.get("/{color}/move")
def move(color:str):
    if(len(students[color])) > indexes[color] + 1:
        indexes[color] +=1

@app.get("/{color}/back")
def move(color:str):
    if indexes[color] > 0:
        indexes[color] -=1

@app.get("/rc/{colour}")
def rc(request:Request, colour):
    return templates.TemplateResponse("rc.html", {"request": request, "name": colour})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)