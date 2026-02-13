import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image_file(file_content: bytes):
    base64_image = base64.b64encode(file_content).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "ハンドメイド専門家として画像を分析し、以下の4つの項目を【必ずJSON形式】で返してください。項目名：'title', 'description', 'price', 'reason' (価格の理由)。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        response_format={ "type": "json_object" } 
    )
    return response.choices[0].message.content