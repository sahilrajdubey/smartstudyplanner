from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pymongo import MongoClient
 
# Connection with mongo db compass
con = MongoClient("mongodb+srv://sahil5661:sahil1234@cluster0.ezqeu4d.mongodb.net/")
db = con["login"]
signup_col = db["signup"]
 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Route to signin page
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="/welcome/welcome.html"
    )
@app.get("/signin", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="/welcome/signin.html")

# Route for signup page
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
  return templates.TemplateResponse(
        request=request, name="/welcome/signup.html"
    )
@app.post("/signup")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    if signup_col.find_one({"email": email}):
        return {"error": "User already exists"}

    signup_col.insert_one({
        "name": name,
        "email": email,
        "password": password  # (We'll hash this later)
    })

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@app.post("/signin", response_class=HTMLResponse)
async def login_user(request: Request, email: str = Form(...), password: str = Form(...)):
    user = signup_col.find_one({"email": email})

    if user and user["password"] == password:
        # Login successful → Show application.html
        return templates.TemplateResponse("/mainapplication/application.html", {
            "request": request,
            "name": user["name"]
        })
    else:
        #  Invalid credentials → Show error on signin page
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid email or password"
        })
@app.get("/upcomingtasks", response_class=HTMLResponse)
def show_upcoming_tasks(request: Request):
    return templates.TemplateResponse("/mainapplication/upcommingtask/upcomingtasks.html", {"request": request, "name": "sahil"})

@app.get("/completedtopics")
def show_completed_topics(request: Request):
    return templates.TemplateResponse("/mainapplication/comtop/completedtopics.html", {"request": request, "name": "sahil"})

@app.get("/progresstracker")
def show_progress_tracker(request: Request):
    return templates.TemplateResponse("/mainapplication/progresstrack/progresstracker.html", {"request": request, "name": "sahil"})

@app.get("/focusmode")
def show_focus_mode(request: Request):
    return templates.TemplateResponse("/mainapplication/focusmodefunc/focusmode.html", {"request": request, "name": "sahil"})

@app.get("/notes")
def show_notes(request: Request):
    return templates.TemplateResponse("/mainapplication/notes/notes.html", {"request": request, "name": "sahil"})

@app.get("/pomodoro")
def show_pomodoro(request: Request):
    return templates.TemplateResponse("/mainapplication/pomodorofunc/pomodoro.html", {"request": request, "name": "sahil"})



db = con["study_planner"]
tasks_col = db["tasks"]
@app.post("/addtask")
async def add_task(
    request: Request,
    task: str = Form(...),
    due_date: str = Form(...),
    priority: str = Form(...)
):
    user = request.session.get("user")
    if user:
        tasks_col.insert_one({
            "user_email": user["email"],
            "task": task,
            "due_date": due_date,
            "priority": priority,
            "status": "pending"
        })
        return RedirectResponse("/upcomingtasks", status_code=303)
    else:
        return RedirectResponse("/", status_code=302)
@app.get("/upcomingtasks", response_class=HTMLResponse)
async def show_upcoming_tasks(request: Request):
    user = request.session.get("user")
    if user:
        user_tasks = list(tasks_col.find({"user_email": user["email"], "status": "pending"}))
        return templates.TemplateResponse("upcomingtasks.html", {
            "request": request,
            "name": user["name"],
            "tasks": user_tasks
        })
    else:
        return RedirectResponse("/", status_code=302)
