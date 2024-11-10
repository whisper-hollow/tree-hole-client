import os
from dotenv import load_dotenv
import audio.asr as asr
from audio.tts import convert_mandarin_to_tailo, create_tailo_voice_file
import services.ai as ai_services
import utils.media as media_utils
import services.line as line_services
from utils.env import update_env_from_google_sheet

load_dotenv()

def initialize_line_service():
    line_service = line_services.create_line_service()
    if line_service:
        print("LINE service initialized successfully")
        line_service.send_text_to_line("LINE service is ready")
    else:
        print("Failed to initialize LINE service")
    return line_service

def main_process(line_service, test_mode=False, test_prompt=None):
    client = ai_services.create_openai_client()

    if test_mode and test_prompt:
        # 測試模式：直接使用提供的文字
        text = os.getenv("RAG_HINT") + ": " + test_prompt
    else:
        # 正常模式：使用語音辨識
        text = asr.recognize_taigi_speech(line_service)

    if text:
        print(f"處理的文字是：{text}")
        line_service.send_text_to_line(f"處理的文字是：{text}")

        # OpenAI 聊天生成文字
        print("RAG 暗示語 ... " + os.getenv("RAG_HINT"))
        if (os.getenv("RAG_HINT") in text):
            print("進入 RAG 模式 ...")
            message_content = ai_services.rag(text)
        else:
            message_content = ai_services.generate_text_from_prompt(client, text)

        if message_content:
            print(message_content)
            line_service.send_text_to_line(message_content)

            # 如果不是測試模式才進行語音合成
            if not test_mode:
                tlpa = convert_mandarin_to_tailo(message_content)
                create_tailo_voice_file(tlpa, os.getenv("DEFAULT_GENDER"), os.getenv("DEFAULT_ACCENT"))
                try:
                    # create output folder if not exists
                    os.makedirs("output", exist_ok=True)
                    media_utils.play_wav("output/synthesized_tlpa_audio.wav")
                except Exception as e:
                    print(f"Failed to play synthesized TLPA audio: {e}")
                    line_service.send_text_to_line(f"無法播放合成的音頻：{e}")

if __name__ == "__main__":
    # 設定測試模式
    TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
    # TEST_PROMPT = "白日依山盡，黃河入海流。欲窮千里目，更上一層樓，這首詩，是什麼顏色？" # 黃色
    TEST_PROMPT = "山中相送罷，日暮掩柴扉。春草明年綠，王孫歸不歸，這首詩，是什麼顏色？。" # 灰色
    # TEST_PROMPT = "遠上寒山石徑斜，白雲生處有人家。停車坐愛楓林晚，霜葉紅於二月花。。這首詩，是什麼顏色？" # 紅色

    line_service = initialize_line_service()
    if not line_service:
        print("無法初始化 LINE 服務，程序退出。")
        exit(1)

    while True:
        if TEST_MODE:
            prompt_message = "測試模式：直接使用預設文字。按下 'Y' 開始，或按任意其他鍵退出："
        else:
            prompt_message = "正常模式：請按下 'Y' 開始，打開麥克風，說完後請關閉麥克風，或按任意其他鍵退出程序："

        print(prompt_message)
        line_service.send_text_to_line(prompt_message)
        update_env_from_google_sheet(os.getenv("GOOGLE_SHEET_KEY"), os.getenv("GOOGLE_SHEET_JSON"))

        try:
            user_input = input().strip().lower()
            if user_input != 'y':
                exit_message = "正在退出程序。"
                print(exit_message)
                line_service.send_text_to_line(exit_message)
                break

            main_process(line_service, TEST_MODE, TEST_PROMPT if TEST_MODE else None)
        except Exception as e:
            error_message = f"發生錯誤：{e}"
            print(error_message)
            line_service.send_text_to_line(error_message)

        print("\n--- 處理完成，準備下一輪 ---\n")