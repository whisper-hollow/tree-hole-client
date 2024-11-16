import os
import speech_recognition as sr
import base64
import requests
import json

# 從環境變數獲取 API URL
TAIGI_ASR_API_URL = os.getenv("TAIGI_ASR_API_URL", "https://speech.bronci.com.tw/ai/taigi/run/predict")

def send_line_message(line_service, message):
    """統一處理 LINE 訊息發送"""
    if os.getenv("LINE_MESSAGE", "true").lower() == "true" and line_service:
        line_service.send_text_to_line(message)

# 台語語音轉文字的函式
def recognize_taigi_speech(line_service):
    recognizer = sr.Recognizer()

    # 使用麥克風錄音
    with sr.Microphone() as source:
        message = "請說，我在聽呢！台語嘛ㄟ通！"
        print(message)
        send_line_message(line_service, message)
        audio = recognizer.listen(source)

    # 將音頻轉換為 WAV 格式並取得 bytes
    audio_data = audio.get_wav_data()

    # 將音頻 bytes 編碼為 base64 字串
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    # API 要求的資料
    payload = {
        "data": [
            {
                "name": "audio.wav",
                "data": f"data:audio/wav;base64,{audio_base64}"
            }
        ]
    }

    # 設定請求標頭
    headers = {
        'accept': '*/*',
        'content-type': 'application/json'
    }

    # 發送 POST 請求到 API
    response = requests.post(TAIGI_ASR_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # 回傳 API 的台語文字
        result = response.json().get('data', [None])[0]
        return result
    else:
        message = f"台語語音轉文字失敗: {response.status_code}"
        print(message)
        send_line_message(line_service, message)
        return None