from fastapi import FastAPI, Depends, UploadFile, File, Request 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models  
import shutil
from database import engine, get_db 
from services import analyze_image_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Craft Lens")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    # DBから全データを取得してHTMLに渡す
    items = db.query(models.Item).order_by(models.Item.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/upload-web")
async def upload_web(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):

    # 1. 画像を指定のフォルダに保存する
    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. 保存した画像を開いてAI分析（servicesに送る）
    with open(file_path, "rb") as f:
        content = f.read()
    ai_result = analyze_image_file(content)
    
    # 3. DB保存（image_urlにフォルダ内のパスを入れる）
    new_item = models.Item(
        title="AI分析作品",
        description=ai_result,
        suggested_price="分析済",
        image_url=f"/{file_path}"
    )
    db.add(new_item)
    db.commit()

    return RedirectResponse(url="/", status_code=303)