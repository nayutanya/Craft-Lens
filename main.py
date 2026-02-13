from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from services import analyze_handmade_image

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