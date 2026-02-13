from fastapi import FastAPI, Depends, UploadFile, File, Request 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models  
import shutil
import json
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

    # 画像保存
    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # AI分析
    with open(file_path, "rb") as f:
        content = f.read()
    ai_raw_result = analyze_image_file(content)
    res = json.loads(ai_raw_result)
    
    # DB保存
    new_item = models.Item(
        title=res.get("title", "無題の作品"),
        description=res.get("description", ""),
        suggested_price=res.get("price", "価格未設定"), 
        image_url=f"/{file_path}"
    )
    db.add(new_item)
    db.commit()

    return RedirectResponse(url="/", status_code=303)

@app.post("/items/{item_id}/delete")
async def delete_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(models.Item).filter(models.Item.id == item_id).first()   
    if item:
        db.delete(item)
        db.commit()

    return RedirectResponse(url="/", status_code=303)