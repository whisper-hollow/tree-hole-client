import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_env_from_google_sheet(sheet_key, json_key_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_key).sheet1  # 打開第一個工作表
    data = sheet.get_all_records()  # 取得所有資料

    if data:
        # 假設我們要使用第一列的資料來更新環境變數
        row = data[0]
        os.environ['NAME'] = row.get('姓名', '預設名子')
        os.environ['DESCRIPTION'] = row.get('描述', '預設描述')
        os.environ['DEFAULT_GENDER'] = row.get('性別', '預設性別')
        os.environ['DEFAULT_ACCENT'] = row.get('腔調', '預設腔調')
        os.environ['DRAW_STYLE'] = row.get('畫畫風格', '預設畫風')