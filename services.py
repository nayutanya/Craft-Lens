import os
import base64
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY is not set.")
client = OpenAI(api_key=api_key)

def analyze_image_file(file_content: bytes, prompt: str):
    base64_image = base64.b64encode(file_content).decode('utf-8')
    full_prompt = f"""
    あなたはプロのハンドメイド作家兼、オンラインマーケットの価格査定人です。
    
    {prompt}

    【出力ルール】
    1. title: 作品の魅力を伝えるタイトル
    2. description: 購入意欲をそそる素敵な説明文
    3. price: 数値のみ。入力された計算根拠がない場合は、画像から「クオリティ・素材・市場相場」をプロ視点で判断し、具体的な販売価格（円）を提示してください。
    4. reason: なぜその価格にしたのか、プロとしての査定理由
    
    【厳守事項】
    - priceは絶対に0や空欄にせず、必ず市場価値に見合った1以上の数値を返してください。
    - 出力は必ず以下の項目を持つ純粋なJSON形式にしてください：'title', 'description', 'price', 'reason'
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": full_prompt
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