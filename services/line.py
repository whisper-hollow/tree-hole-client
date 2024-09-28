import os
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage

class LineService:
    def __init__(self):
        self.channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
        self.user_id = os.getenv("USER_ID")
        
        if not self.channel_access_token:
            raise ValueError("CHANNEL_ACCESS_TOKEN is not set in environment variables")
        
        if not self.user_id:
            raise ValueError("USER_ID is not set in environment variables")
        
        self.line_bot_api = LineBotApi(self.channel_access_token)

    def send_text_to_line(self, text):
        try:
            message = TextSendMessage(text=text)
            self.line_bot_api.push_message(self.user_id, message)
            print("Text message sent to LINE Bot successfully.")
        except Exception as e:
            print(f"Error sending text message to LINE: {e}")

    def send_image_to_line(self, image_url):
        try:
            message = ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            )
            self.line_bot_api.push_message(self.user_id, message)
            print("Image sent to LINE Bot successfully.")
        except Exception as e:
            print(f"Error sending image to LINE: {e}")

def create_line_service():
    try:
        return LineService()
    except ValueError as e:
        print(f"Error creating LineService: {e}")
        return None