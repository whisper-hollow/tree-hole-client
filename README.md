# 樹洞

「樹洞」是一個象徵人們傾訴心事的安全空間，代表著一個可以隨時分享秘密和心事的對象或地方。這個概念來自於傳說或文學作品，樹洞不會洩露秘密，提供一個情感的出口和心靈的釋放。

在這個專案中，我們將這個概念進一步結合現代技術，實現以下三個核心功能：

1. **國語、台語雙軌語音辨識：**
   - 讓「樹洞」不僅能理解國語，還能精準辨識台語，為多語言使用者提供更加自然、無障礙的交流方式。
  
2. **串接大語言模型（LLM）：**
   - 樹洞不僅能聆聽與理解使用者的心事，還能透過大語言模型生成適當的回應，提供智慧化的情感陪伴。無論是安慰、建議，還是提供知識性的回應，都將通過這個模型實現。

3. **代理人機制觸發第三方 API：**
   - 在陪伴使用者的過程中，樹洞會以代理人（agent）的形式，根據使用者的需求或情境，觸發第三方 API，進行更深入的互動。例如，在使用者情緒低落時，觸發日程提醒、物聯網裝置等服務，以提供更貼心的支持。

「樹洞」系統不僅僅是一個單向的情感宣洩工具，而是一個多元化、智慧化的互動平台，能夠在不同語言、不同需求的基礎上，持續陪伴並提供適時的幫助。

## 參考資料
- 本專案受到以下專案啟發：
  - 國立師範大學 - 科技 113 - 許慧儀
  - [數位孿生應用 : 跟自己對話 - 回憶殺](https://www.canva.com/design/DAF26lRORQo/75FnAs7g22F4bW2xTaxAdA/view?utm_content=DAF26lRORQo&utm_campaign=designshare&utm_medium=link&utm_source=editor#2)

## 系統架構
![系統架構](https://github.com/user-attachments/assets/6f75b0a7-1add-4fd1-bb0b-87afe24200f7)

## 安裝
```bash=
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

## 執行
```bash=
python3 main.py
```

## 展示
- https://www.youtube.com/watch?v=LUbgPd-3NSc

## 教材
- https://hackmd.io/@yillkid/rkXPxAQ0R
