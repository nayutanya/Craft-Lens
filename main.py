from fastapi import FastAPI, Depends
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from services import analyze_image_file

# 起動時にデータベーステーブルを作成する
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Craft Lens API is running!"}

@app.get("/test-ai-save")
def test_ai_save(db: Session = Depends(get_db)):
    # 1. テスト用の画像URL
    test_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
    
    # 2. AIで分析
    ai_result = analyze_handmade_image(test_url)
    
    # 3. DBに保存するデータを作成
    # 本来はAIの回答をパース（分割）すべきですが、まずは全文をdescriptionに入れます
    new_item = models.Item(
        title="AI分析テスト作品",
        description=ai_result,
        suggested_price="分析結果を参照",
        image_url=test_url
    )
    
    # 4. DBに書き込み
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {"status": "saved", "item": new_item}

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    # データベースから全件取得する
    items = db.query(models.Item).all()
    return items

@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    # データベースに保存されている全作品を取得する
    items = db.query(models.Item).all()
    return items

from fastapi import UploadFile, File # 冒頭のimportに追加

@app.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. アップロードされた画像を読み込む
    content = await file.read()
    
    # 2. AIで解析
    ai_result = analyze_image_file(content)
    
    # 3. DBに保存
    new_item = models.Item(
        title="アップロード作品",
        description=ai_result,
        suggested_price="分析結果を参照",
        image_url="local_upload" # 今回は簡易的に
    )
    db.add(new_item)
    db.commit()
    
    return {"message": "分析完了！DBに保存しました", "analysis": ai_result}