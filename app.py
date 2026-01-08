import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="歐拉夫奶茶日誌", page_icon="🐾", layout="centered")

# --- 深度自訂 CSS：全方位奶茶色 ---
st.markdown("""
    <style>
    /* 整體底色 */
    .main { background-color: #F3E9DC; }
    
    /* 標題與文字 */
    h1, h3, h4 { color: #8E735B !important; font-family: "Microsoft JhengHei", sans-serif; text-align: center; }
    p { color: #A68A64; }

    /* 表單樣式 */
    .stForm { 
        border: 2px solid #DDBEAA !important; 
        border-radius: 25px !important; 
        background-color: #FFFFFF !important; 
    }

    /* 按鈕樣式 */
    .stButton>button { 
        background-color: #C6AC8F; color: white; border-radius: 20px; 
        border: none; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #8E735B; color: white; }

    /* --- 日曆深度奶茶化 --- */
    /* 1. 日曆標頭背景與文字 */
    .fc-header-toolbar { color: #8E735B; font-weight: bold; }
    
    /* 2. 日曆格子背景與邊框 */
    .fc-theme-standard td, .fc-theme-standard th { border-color: #EAE2D6 !important; }
    .fc-daygrid-day-number { color: #8E735B !important; text-decoration: none !important; }
    
    /* 3. 今天的格子背景 */
    .fc-day-today { background-color: #EAE2D6 !important; }
    
    /* 4. 運動標籤 (Event) */
    .fc-event { 
        background-color: #C6AC8F !important; 
        border: none !important; 
        border-radius: 8px !important;
        padding: 2px !important;
    }
    
    /* 5. 選中的日期框 (Highlight) */
    .fc-highlight { background-color: #DDBEAA !important; opacity: 0.3 !important; }

    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🍦 歐拉夫動一動 🍦</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 2. 紀錄表單 ---
with st.form(key="olaf_workout_form", clear_on_submit=True):
    st.markdown
