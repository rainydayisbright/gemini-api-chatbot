from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# โหลดค่าจากไฟล์ .env
load_dotenv()

app = FastAPI()

# ตั้งค่า API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """โหลดหน้า HTML"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(prompt: str = Form(...)):
    """รับข้อความจากผู้ใช้ -> ส่งให้ Gemini -> ส่งกลับคำตอบ"""
    try:
        # สร้าง Client ของ Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # ส่งข้อความเข้าโมเดล
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            )
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ใช้โมเดลที่มีจริง
            contents=contents,
        )

        # ดึงข้อความตอบกลับ
        message = response.candidates[0].content.parts[0].text

        return JSONResponse({"response": message})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
