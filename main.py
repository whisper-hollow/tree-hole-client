import os
from dotenv import load_dotenv
import audio.asr as asr
from audio.tts import convert_mandarin_to_tailo, create_tailo_voice_file
import services.ai as ai_services
import utils.media as media_utils
import services.line as line_services

load_dotenv()

def main_process(line_service):
    client = ai_services.create_openai_client()

    # 語音轉文字，改為台語語音轉文字
    text = asr.recognize_taigi_speech(line_service)  # 傳遞 line_service
    if text:
        print(f"我聽到的是：{text}")
        line_service.send_text_to_line(f"我聽到的是：{text}")

        # OpenAI 聊天生成文字
        message_content = ai_services.generate_text_from_prompt(client, text)
        if message_content:
            print(message_content)
            line_service.send_text_to_line(message_content)

            # 語音合成（但不立即播放）
            tlpa = convert_mandarin_to_tailo(message_content)
            gender = os.getenv("DEFAULT_GENDER")
            accent = os.getenv("DEFAULT_ACCENT")
            create_tailo_voice_file(tlpa, gender, accent)

        # 使用 OpenAI API 生成圖片
        image_url = ai_services.generate_image_from_text(client, "請以繪本的風格產生圖片，提示詞：" + text)
        if image_url:
            print(f"Generated image URL: {image_url}")
            save_path = "output/generated_image.png"
            media_utils.download_image(image_url, save_path)

            # 發送圖片到 LINE
            line_service.send_image_to_line(image_url)

        # 在生成圖片後播放 WAV 檔
        if message_content:
            try:
                media_utils.play_wav("output/synthesized_tlpa_audio.wav")
            except Exception as e:
                print(f"Failed to play synthesized TLPA audio: {e}")
                line_service.send_text_to_line(f"無法播放合成的音頻：{e}")

def initialize_line_service():
    line_service = line_services.create_line_service()
    if line_service:
        print("LINE service initialized successfully")
        line_service.send_text_to_line("LINE service is ready")
    else:
        print("Failed to initialize LINE service")
    return line_service

if __name__ == "__main__":
    line_service = initialize_line_service()
    if not line_service:
        print("無法初始化 LINE 服務，程序退出。")
        exit(1)

    while True:
        prompt_message = "請按下 'Y' 開始，打開麥克風，說完後請關閉麥克風，或按任意其他鍵退出程序："
        print(prompt_message)
        line_service.send_text_to_line(prompt_message)
        
        try:
            user_input = input().strip().lower()
            if user_input != 'y':
                exit_message = "正在退出程序。"
                print(exit_message)
                line_service.send_text_to_line(exit_message)
                break
            
            main_process(line_service)
        except Exception as e:
            error_message = f"發生錯誤：{e}"
            print(error_message)
            line_service.send_text_to_line(error_message)
        
        print("\n--- 處理完成，準備下一輪 ---\n")