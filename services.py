import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image_file(file_content: bytes):
    # 画像データをAIが読める形式（base64）に変換
    base64_image = base64.b64encode(file_content).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "ハンドメイド専門家として、この作品の『魅力的な商品名』『商品説明文』『価格目安』を日本語で提案してください。"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content