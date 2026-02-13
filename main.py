from fastapi import FastAPI, Depends, UploadFile, File, Request 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import models  
from database import engine, get_db # 
from services import analyze_image_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Craft Lens")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    # DBから全データを取得してHTMLに渡す
    items = db.query(models.Item).order_by(models.Item.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/upload-web")
async def upload_web(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    ai_result = analyze_image_file(content)
    
    new_item = models.Item(
        title="AI分析作品",
        description=ai_result,
        suggested_price="分析済",
        image_url="local_upload"
    )
    db.add(new_item)
    db.commit()
    
    # 保存したらトップページにリダイレクト（戻る）
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/", status_code=303)