import streamlit as st
import pandas as pd

# 1. 設定網頁標題與寬版顯示
st.set_page_config(page_title="碳足跡資料庫搜尋系統", layout="wide")

# 2. 網頁主標題
st.title("🌱 台灣磁原科技 - Ecoinvent 資料庫查詢系統")
st.markdown("這是一個進階的資料查詢介面，您可以透過左側選單進行搜尋與篩選。")

# 3. 讀取 Excel 檔案
@st.cache_data
def load_data():
    df = pd.read_excel("econinvent1.xlsx")
    return df

try:
    df = load_data()
    
    # --- 左側邊欄：搜尋與篩選介面 ---
    st.sidebar.header("🔍 資料篩選器")
    search_query = st.sidebar.text_input("輸入關鍵字 (例如：材料名稱或代碼)")

    # --- 處理資料過濾邏輯 ---
    filtered_df = df.copy()
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    # --- 主畫面：顯示結果 ---
    st.subheader(f"📊 查詢結果 (共 {len(filtered_df)} 筆資料)")
    st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 找不到 `ecoinvent1.xlsx` 檔案，請確認檔案名稱是否正確。")
except Exception as e:
    st.error(f"⚠️ 發生錯誤：{e}")
