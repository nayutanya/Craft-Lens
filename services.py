import os
import base64
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY is not set.")
client = OpenAI(api_key=api_key)

def analyze_image_file(file_content: bytes, prompt: str):
    base64_image = base64.b64encode(file_content).decode('utf-8')
    full_prompt = f"{prompt}\n\n出力は必ず以下の項目を持つJSON形式にしてください：'title', 'description', 'price', 'reason'"

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