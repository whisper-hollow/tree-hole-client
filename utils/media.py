import requests
import pygame
import time

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image successfully saved to {save_path}")
        else:
            print("Failed to retrieve image from URL.")
    except Exception as e:
        print(f"Error downloading image: {e}")

def play_wav(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        print("Audio playback completed.")
    except Exception as e:
        print(f"Error playing wav file: {e}")