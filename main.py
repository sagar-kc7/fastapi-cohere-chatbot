from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cohere

app = FastAPI()
co = cohere.Client("SjGQulQI2EDojS9ew77SxVkEc7e1MbsM8JFSdlRv")  # 🔐 Replace this with your actual key

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def serve_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Using Cohere's generate endpoint (you can use `chat()` if your plan supports it)
    response = co.generate(
        model='command-r-plus',  # or 'command-r' / 'command-light' / 'command-nightly'
        prompt=user_message,
        max_tokens=100,
        temperature=0.7,
    )

    reply = response.generations[0].text.strip()
    return JSONResponse(content={"reply": reply})
