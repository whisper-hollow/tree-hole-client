# 樹洞

「樹洞」象徵著一個安全的傾訴空間，在這裡人們可以分享心事和秘密。這個概念源自於傳統文化中樹洞作為守密者的意象，我們將其現代化並結合科技，實現以下核心功能：

1. **雙語語音辨識**
   - 支援國語及台語的語音辨識
   - 提供更自然的使用者交流體驗

2. **大語言模型整合**
   - 透過 LLM 提供智慧化情感陪伴
   - 生成合適的回應與建議

3. **智慧代理人系統**
   - 根據情境觸發第三方 API
   - 提供個人化的互動服務

## 參考資料
- 國立師範大學 - 科技 113 - 許慧儀
- [數位孿生應用：跟自己對話 - 回憶殺](https://www.canva.com/design/DAF26lRORQo/75FnAs7g22F4bW2xTaxAdA/view)

## 系統架構
![系統架構](https://github.com/user-attachments/assets/6f75b0a7-1add-4fd1-bb0b-87afe24200f7)

## 安裝
```bash
# 創建環境
python3 -v venv venv

# 進入環境
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安裝套件
pip3 install -r requirements.txt
```

## 執行
```bash
python3 main.py
```

## 展示
- [示範影片](https://www.youtube.com/watch?v=LUbgPd-3NSc)

## 教材
- [技術文件](https://hackmd.io/@yillkid/rkXPxAQ0R)

# 環境變數說明

### 基礎設定
用於控制系統運作模式
- `TEST_MODE`: 測試模式開關
  - 預設值: `false`
  - 用途: 啟用時跳過語音辨識，使用預設文字

### LINE 機器人設定
LINE Bot 連線驗證資訊
- `CHANNEL_ACCESS_TOKEN`: LINE 頻道存取權杖
- `CHANNEL_SECRET`: LINE 頻道密鑰
- `USER_ID`: LINE 使用者識別碼

### 語音服務設定
台語語音合成參數
- `HOST_ASR_TTL_TAILO`: 語音服務位址
  - 範例: `http://tts001.iptcloud.net:8804`
- `DEFAULT_GENDER`: 語音性別
  - 可選: `女聲`, `男聲`
- `DEFAULT_ACCENT`: 口音設定
  - 可選: `強勢腔（高雄腔）` 等

### 數位分身設定
角色個性與外觀設定
- `GOOGLE_SHEET_KEY`: 數位分身資料表 ID
- `GOOGLE_SHEET_JSON`: API 憑證路徑
  - 預設: `secrets/google_sheet.json`
- `NAME`: 角色名稱
  - 範例: `小檸檬`
- `DESCRIPTION`: 角色個性
  - 範例: `我叫小檸檬，只愛跳舞，不喜歡睡覺。`
- `DRAW_STYLE`: 繪圖風格
  - 範例: `繪本`

### RAG 設定
知識庫連接設定
- `URL_LLMTWINS`: 服務端點
  - 範例: `https://beta-llmtwins.4impact.cc/prompt`
- `RAG_ROLE`: 角色設定
  - 範例: `AI 貓咪`
- `RAG_HINT`: 觸發關鍵字
  - 範例: `檸檬`

### 注意事項
安全性提醒
- 將敏感資料存於 `.env`
- 設定 `.gitignore` 排除 `.env`
- 參考 `.env.example`
