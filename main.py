import os
from dotenv import load_dotenv
import audio.asr as asr
from audio.tts import convert_mandarin_to_tailo, create_tailo_voice_file
import services.ai as ai_services
import utils.media as media_utils
import services.line as line_services
from utils.env import update_env_from_google_sheet

load_dotenv()

def send_line_message(line_service, message):
    """統一處理 LINE 訊息發送"""
    if os.getenv("LINE_MESSAGE", "true").lower() == "true" and line_service:
        line_service.send_text_to_line(message)

def initialize_line_service():
    """初始化 LINE 服務"""
    line_service = line_services.create_line_service()
    if line_service:
        print("LINE service initialized successfully")
        send_line_message(line_service, "LINE service is ready")
        return line_service
    print("Failed to initialize LINE service")
    return None

def process_audio_response(message_content, line_service, test_mode):
    """處理音頻回應"""
    try:
        if not test_mode:
            tlpa = convert_mandarin_to_tailo(message_content)
            create_tailo_voice_file(tlpa, os.getenv("DEFAULT_GENDER"), os.getenv("DEFAULT_ACCENT"))
            os.makedirs("output", exist_ok=True)
            media_utils.play_wav("output/synthesized_tlpa_audio.wav")
    except Exception as e:
        error_msg = f"無法播放合成的音頻：{e}"
        print(error_msg)
        send_line_message(line_service, error_msg)

def main_process(line_service, test_mode=False, test_prompt=None):
    """主要處理邏輯"""
    # 獲取輸入文字
    input_text = test_prompt if test_mode and test_prompt else asr.recognize_taigi_speech(line_service)

    if not input_text:
        return

    # 處理輸入文字
    print(f"處理的文字是：{input_text}")
    send_line_message(line_service, f"處理的文字是：{input_text}")

    # 生成回應
    message_content = ai_services.rag(input_text)
    if message_content:
        print(message_content)
        send_line_message(line_service, message_content)
        process_audio_response(message_content, line_service, test_mode)

def run_main_loop(line_service):
    """主循環"""
    TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
    TEST_PROMPT = "遠上寒山石徑斜，白雲生處有人家。停車坐愛楓林晚，霜葉紅於二月花。。這首詩，是什麼顏色？"

    while True:
        prompt_message = (
            "測試模式：直接使用預設文字。按下 'Y' 開始，或按任意其他鍵退出："
            if TEST_MODE else
            "正常模式：請按下 'Y' 開始，打開麥克風，說完後請關閉麥克風，或按任意其他鍵退出程序："
        )

        print(prompt_message)
        send_line_message(line_service, prompt_message)
        update_env_from_google_sheet(os.getenv("GOOGLE_SHEET_KEY"), os.getenv("GOOGLE_SHEET_JSON"))

        try:
            if input().strip().lower() != 'y':
                exit_message = "正在退出程序。"
                print(exit_message)
                send_line_message(line_service, exit_message)
                break

            main_process(line_service, TEST_MODE, TEST_PROMPT if TEST_MODE else None)
        except Exception as e:
            error_message = f"發生錯誤：{e}"
            print(error_message)
            send_line_message(line_service, error_message)

        print("\n--- 處理完成，準備下一輪 ---\n")

if __name__ == "__main__":
    line_service = initialize_line_service()
    if not line_service:
        print("無法初始化 LINE 服務，程序退出。")
        exit(1)

    run_main_loop(line_service)