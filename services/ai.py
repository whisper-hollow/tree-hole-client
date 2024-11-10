import os
import json
import requests
from openai import OpenAI

def generate_image_from_text(client, prompt, size="1024x1024"):
    try:
        # 從環境變數中獲取 DRAW_STYLE
        draw_style = os.getenv('DRAW_STYLE', '預設風格')

        # 將 DRAW_STYLE 整合到 prompt 中
        full_prompt = f"請以 {draw_style} 風格生成圖片。提示詞：{prompt}"

        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size=size,
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def generate_text_from_prompt(client, prompt, model="gpt-4o", max_tokens=256):
    try:
        # 從環境變數中獲取 AI 的 NAME 和 DESCRIPTION
        name = os.getenv('NAME', '預設名子')
        description = os.getenv('DESCRIPTION', '預設描述')

        # 將 NAME 和 DESCRIPTION 整合到 prompt 中，描述 AI 自己
        full_prompt = f"我的名字叫做 {name}，{description}。現在回答：{prompt} (請用正體中文(zh_TW)回答)"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=1,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message_content = response.choices[0].message.content
        return message_content
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def rag(prompt):
    payload = json.dumps({
      "role": os.getenv("RAG_ROLE"),
      "type": "RAG",
       "tools": [{"tool":"agent","load_tools":"custom"}],
      "message": prompt
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", os.getenv("URL_LLMTWINS"), headers=headers, data=payload)

    # Convert response to JSON
    try:
        response = response.json()
        return response["message"]
    except Exception as e:
        print(str(e))
        return f"{os.getenv('RAG_ROLE')}壞掉了，趕快請黃檸爸爸來修理: " + str(e)

def create_openai_client():
    return OpenAI()
