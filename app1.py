import streamlit as st
import pandas as pd
import os

# 1. 網頁基本設定
st.set_page_config(page_title="SSBTi 碳排查詢系統", layout="wide")
st.title("🌱 SSBTi 碳排係數查詢系統")
st.subheader("汪瑞民 (Raymond Wang) 執行長專用版 - 台灣磁原科技")
st.markdown("---")

excel_file = 'econinvent1.xlsx'

if os.path.exists(excel_file):
    try:
        # 讀取 Excel
        @st.cache_data
        def load_data():
            return pd.read_excel(excel_file, engine='openpyxl')
        
        df = load_data()
        st.success(f"✅ 資料庫載入成功！目前共有 {len(df)} 筆數據。")
        
        # 💡 【診斷工具】直接印出您真實的欄位名稱
        st.info(f"📋 系統偵測到您的 Excel 實際欄位名稱如下：\n {list(df.columns)}")
        
        # 3. 搜尋功能
        query = st.text_input("🔍 請輸入關鍵字搜尋", placeholder="輸入後按下 Enter...")
        
        if query:
            # 萬用搜尋法：不再指定特定欄位，只要這橫列任何一個格子有關鍵字就抓出來
            mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
            results = df[mask]
            
            st.write(f"📊 找到 {len(results)} 筆相符結果：")
            st.dataframe(results, use_container_width=True)
                
    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.warning(f"⚠️ 找不到檔案：{excel_file}。請確認檔案已放入 SSBTi 資料夾。")

st.markdown("---")
st.caption("© 2026 汪瑞民 Raymond Wang | 台灣磁原科技 | 科學減碳協會 (SSBTi)")
