import streamlit as st
from datetime import date
from datetime import datetime
from google.oauth2 import service_account
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


# Google Sheets APIの認証
def get_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file"
    ]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
    client = gspread.authorize(creds)
    return client

# User認証
def authenticate_user(user_id, password, sheet):
    try:
        records = sheet.get_all_records()  # 全レコード取得
        for record in records:
            # IDとパスワードの比較時に型を統一
            if record["ID"] == user_id and str(record["pass"]) == str(password):
                return True
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False


# メインコンテンツ
st.markdown('<div class="main-content">', unsafe_allow_html=True)

def main():

    # Googleスプレッドシート接続
    client = get_gspread_client()

    # ログイン画面
    if 'logged_in' not in st.session_state:
        st.image('img/logo.png')
        user_sheet = client.open_by_url(user_sheet_url).sheet1
        user_id = st.text_input("ユーザーID", value="")
        password = st.text_input("パスワード", value="", type="password")
        if st.button("ログイン"):
            if authenticate_user(user_id, password, user_sheet):
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.page = 'トップ画面'
                st.rerun()  
            else:
                st.error("ログイン失敗: ユーザーIDまたはパスワードが間違っています。")
        return
    
    # デフォルトのマイルを session_state に設定
    if 'miles' not in st.session_state:
        mile_sheet = client.open_by_url(mile_sheet_url).sheet1
        # ユーザーの最新マイル情報を取得
        latest_mile = get_latest_mile(st.session_state.user_id, mile_sheet)
        st.session_state.miles = int(latest_mile)  # ここでint型に変換
    

    # Navigation based on the session state
    page = st.session_state.get('page', 'トップ画面')
    
    if page == 'トップ画面':
        top_page()
    elif page == 'プラン選択':
        plan_selection_page()
    elif page == 'マイル登録':
        miles_page()
    elif page == 'フィードバック':
        feedback_page()
    elif page == '交換しました':
        exchange_success_page()

