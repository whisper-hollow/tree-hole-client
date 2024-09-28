import os
import requests

# 從環境變數獲取 HOST
HOST = os.getenv("HOST_ASR_TTL_TAILO", "http://tts001.iptcloud.net:8804")

# 合成語音檔
def synthesize(text0):
    url = f"{HOST}/synthesize_text?text0={requests.utils.quote(text0)}"
    response = requests.get(url, headers={"Cache-Control": "no-cache"})
    if response.status_code == 200:
        with open("output/synthesized_audio.wav", "wb") as f:
            f.write(response.content)
        print("Synthesized audio saved as synthesized_audio.wav")
    else:
        print(f"Failed to synthesize text. Status code: {response.status_code}")

# 國語轉台羅
def convert_mandarin_to_tailo(text):
    url = f"{HOST}/display?text0={requests.utils.quote(text)}"
    response = requests.get(url)
    if response.status_code == 200:
        print("TLPA display:")
        print(response.text)
        return response.text
    else:
        print(f"Failed to get TLPA display. Status code: {response.status_code}")

# 合成台羅音檔
def create_tailo_voice_file(text, gender, accent):
    url = f"{HOST}/synthesize_TLPA?text1={requests.utils.quote(text)}&gender={requests.utils.quote(gender)}&accent={requests.utils.quote(accent)}"
    response = requests.get(url, headers={"Cache-Control": "no-cache"})
    if response.status_code == 200:
        with open("output/synthesized_tlpa_audio.wav", "wb") as f:
            f.write(response.content)
        print("Synthesized TLPA audio saved as synthesized_tlpa_audio.wav")
    else:
        print(f"Failed to synthesize TLPA text. Status code: {response.status_code}")

def display2taibun(text0):
    url = f"{HOST}/display2taibun?text0={requests.utils.quote(text0)}"
    response = requests.get(url)
    if response.status_code == 200:
        print("漢羅台文 display:")
        print(response.text)
    else:
        print(f"Failed to get 漢羅台文 display. Status code: {response.status_code}")

def display2(text0):
    url = f"{HOST}/display2?text0={requests.utils.quote(text0)}"
    response = requests.get(url)
    if response.status_code == 200:
        print("台羅拼音 display:")
        print(response.text)
    else:
        print(f"Failed to get 台羅拼音 display. Status code: {response.status_code}")

# 測試用例
if __name__ == "__main__":
    # FIXME: 測試 synthesize
    text_to_synthesize = "媽媽，今天天氣很好，我們一起出去玩。"
    # synthesize(text_to_synthesize)

    # 測試 convert_mandarin_to_tailo
    tlpa = convert_mandarin_to_tailo(text_to_synthesize)
    # print("kin1-a2-jit8 thinn1-khi3 tsin1 ho2, lan2 tso3-hue2 tshut4-khi3 tshit4-tho5.")

    # GOOD: 測試 create_tailo_voice_file
    # text_to_synthesize_tlpa = "kin1-a2-jit8 thinn1-khi3 tsin1 ho2, lan2 tso3-hue2 tshut4-khi3 tshit4-tho5."
    gender = "女聲"
    accent = "強勢腔（高雄腔）"
    # create_tailo_voice_file(text_to_synthesize_tlpa, gender, accent)
    create_tailo_voice_file(tlpa, gender, accent)

    # 測試 display2taibun
    # display2taibun(text_to_synthesize)

    # 測試 display2
    # display2(text_to_synthesize_tlpa)