import streamlit as st
import pandas as pd

# 1. 設定網頁標題與寬版顯示
st.set_page_config(page_title="碳足跡資料庫搜尋系統", layout="wide")

# 2. 網頁主標題
st.title("🌱 台灣磁原科技 - Ecoinvent 資料庫查詢系統")
st.markdown("這是一個進階的資料查詢介面，您可以透過左側選單進行多重搜尋與精確篩選。")

# 3. 讀取 Excel 檔案 (使用快取加速)
@st.cache_data
def load_data():
    df = pd.read_excel("econinvent1.xlsx")
    return df

try:
    df = load_data()
    
    # --- 左側邊欄：搜尋與篩選介面 ---
    st.sidebar.header("🔍 資料篩選器")
    
    # 🌟 功能一：保留原本的「關鍵字搜尋」
    search_query = st.sidebar.text_input("1️⃣ 輸入關鍵字 (全表搜尋)")

    st.sidebar.markdown("---")
    
    # 🌟 功能二：新增「動態下拉式選單」
    st.sidebar.subheader("2️⃣ 進階下拉篩選")
    st.sidebar.markdown("請先選擇要篩選的『欄位』，再選擇『內容』：")
    
    # 讓系統自動讀取 Excel 的所有欄位名稱
    all_columns = df.columns.tolist()
    
    # 讓使用者挑選要用哪個欄位來篩選
    selected_column = st.sidebar.selectbox("選擇篩選欄位 (如：地區、單位、分類)", ["(不使用)"] + all_columns)
    
    selected_items = []
    if selected_column != "(不使用)":
        # 抓出該欄位所有不重複的內容選項
        unique_values = df[selected_column].dropna().astype(str).unique().tolist()
        # 建立多重選擇下拉選單 (可以一次勾選多個項目)
        selected_items = st.sidebar.multiselect(f"請勾選 {selected_column} 的項目：", unique_values)

    # --- 處理資料過濾邏輯 ---
    filtered_df = df.copy()
    
    #
