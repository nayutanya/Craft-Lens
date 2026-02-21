import os
import models  
import shutil
import json
from fastapi import FastAPI, Depends, UploadFile, File, Request, Form
from prompts import SYSTEM_PROMPT_TEMPLATE, LENGTH_MAPPING
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
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

@app.get("/items/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    # IDに一致するアイテムを1つだけ取得
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    # もしアイテムがなければ404エラー（またはトップへリダイレクト）
    if item is None:
        return RedirectResponse(url="/", status_code=303)
        
    return templates.TemplateResponse("detail.html", {"request": request, "item": item})

@app.post("/upload-web")
async def upload_web(request: Request, file: UploadFile = File(...), length: str = Form("medium"), material_cost: int = Form(0), work_hours: float = Form(0.0), db: Session = Depends(get_db)):

    # 価格計算
    base_price = (material_cost * 3) + (work_hours * 1100) 
    price_logic = f"材料費({material_cost}円)の3倍に、作業時間({work_hours}時間)分の技術料を加味した合計{int(base_price)}円をベースに算出してください。"
    
    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        length_instruction=LENGTH_MAPPING.get(length, LENGTH_MAPPING["medium"]),
        price_logic=price_logic
    )

    # 画像保存
    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # AI分析
    with open(file_path, "rb") as f:
        content = f.read()
    ai_raw_result = analyze_image_file(content, prompt)
    res = json.loads(ai_raw_result)
    
    # DB保存
    new_item = models.Item(
        title=res.get("title", "無題の作品"),
        description=res.get("description", ""),
        suggested_price=res.get("price", str(int(base_price))), 
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

@app.post("/analyze")
async def analyze_craft(
    file: UploadFile = File(...),
    length: str = Form("medium"),
    material_cost: int = Form(0),
    work_hours: float = Form(0.0)
):
    # 1. 価格計算ロジック
    base_price = (material_cost * 3) + (work_hours * 1100)
    price_logic = f"材料費({material_cost}円)の3倍に、作業時間({work_hours}時間)分の技術料を加味し、合計{int(base_price)}円前後をベースに市場相場を考慮してください。"

    # 2. プロンプトの組み立て
    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        length_instruction=LENGTH_MAPPING.get(length, LENGTH_MAPPING["medium"]),
        price_logic=price_logic
    )
    return {"analysis": "AIの回答結果", "suggested_price": int(base_price)}