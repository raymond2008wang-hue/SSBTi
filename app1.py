import streamlit as st
import pandas as pd

# 1. 設定網頁標題與寬版顯示
st.set_page_config(page_title="碳足跡資料庫搜尋系統", layout="wide")

# 2. 網頁主標題
st.title("🌱 SSBTi.org-Ecoinvent3.9.1 足跡數據搜尋系統-by Nanozeo.com")
st.markdown("這是一個進階的資料查詢介面，您可以透過左側選單進行多重搜尋與精確篩選。")

# 3. 讀取 Excel 檔案
@st.cache_data
def load_data():
    df = pd.read_excel("econinvent1.xlsx")
    return df

try:
    df = load_data()
    
    # --- 左側邊欄：搜尋與篩選介面 ---
    st.sidebar.header("🔍 資料篩選器")
    
    search_query = st.sidebar.text_input("1️⃣ 輸入關鍵字 (全表搜尋)")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("2️⃣ 進階下拉篩選")
    st.sidebar.markdown("請先選擇要篩選的『欄位』，再選擇『內容』：")
    
    all_columns = df.columns.tolist()
    selected_column = st.sidebar.selectbox("選擇篩選欄位 (如：Geography, Sector)", ["(不使用)"] + all_columns)
    
    selected_items = []
    if selected_column != "(不使用)":
        unique_values = df[selected_column].dropna().astype(str).unique().tolist()
        selected_items = st.sidebar.multiselect(f"請勾選 {selected_column} 的項目：", unique_values)

    # --- 處理資料過濾邏輯 ---
    filtered_df = df.copy()
    
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]
        
    if selected_column != "(不使用)" and len(selected_items) > 0:
        filtered_df = filtered_df[filtered_df[selected_column].astype(str).isin(selected_items)]

    # --- 🌟 核心修改：重新排列顯示欄位順序 🌟 ---
    # 定義您希望優先顯示的欄位清單 (此處採用 Ecoinvent 常見的英文首字母大寫格式)
    priority_cols = [
        "Activity Name",
        "Geography",
        "Time Period",
        "Special Activity Type",
        "Sector"
    ]
    
    # 為了避免 Excel 欄位名稱大小寫差異導致系統當機，我們寫一個保護機制：
    # 只挑選「確實存在於 Excel 表格中」的優先欄位
    actual_priority = [col for col in priority_cols if col in filtered_df.columns]
    
    # 找出其他所有剩下的欄位
    other_cols = [col for col in filtered_df.columns if col not in actual_priority]
    
    # 組合新的欄位順序：優先欄位排前面，剩下的排後面
    final_column_order = actual_priority + other_cols
    
    # 套用新的欄位順序到要顯示的資料表上
    display_df = filtered_df[final_column_order]

    # --- 主畫面：顯示結果 ---
    st.subheader(f"📊 查詢結果 (共 {len(display_df)} 筆資料) * 資料較多，你可以用游標移動資料欄位查看；可以截屏提交顧問取得最新足跡報告")
    st.dataframe(display_df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 找不到 `econinvent1.xlsx` 檔案，請確認檔案名稱是否正確。")
except Exception as e:
    st.error(f"⚠️ 發生錯誤：{e}")
