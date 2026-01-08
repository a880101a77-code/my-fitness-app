import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="小熊健身日誌", page_icon="🧸", layout="centered")

# --- 可愛風格 CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFF9FB; }
    h1 { color: #FF85A2; font-family: "Microsoft JhengHei", sans-serif; text-align: center; }
    .stButton>button { 
        background-color: #FFB3C6; color: white; border-radius: 20px; 
        width: 100%; border: none; font-weight: bold;
    }
    .stForm { border: 2px solid #FFE5EC !important; border-radius: 25px !important; background-color: white !important; }
    /* 日曆字體顏色調整 */
    .fc-event { border: none !important; background-color: #FFB3C6 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>☁️ 健身小日常 ☁️</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料儲存 (暫時存在 Session 中) ---
if 'events' not in st.session_state:
    st.session_state['events'] = []

# --- 2. 快速打卡表單 ---
with st.form(key="quick_check_in", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 快速打卡</h3>", unsafe_allow_html=True)
    
    col_d, col_e = st.columns([1, 1])
    with col_d:
        d = st.date_input("日期", datetime.now())
    with col_e:
        ex_name = st.text_input("運動項目", placeholder="例如：慢跑")
    
    col1, col2 = st.columns(2)
    with col1:
        s = st.number_input("組數", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("次數/重量", min_value=1, step=1, value=12)
    
    submitted = st.form_submit_button("完成訓練，送出愛心 🐾")

if submitted:
    # 將新紀錄加入日曆事件清單
    new_event = {
        "title": f"✨ {ex_name}",
        "start": d.isoformat(),
        "end": d.isoformat(),
        "allDay": True,
    }
    st.session_state['events'].append(new_event)
    st.balloons()
    st.success(f"🌷 紀錄成功！")

st.divider()

# --- 3. 運動日曆視圖 ---
st.markdown("<h3 style='color: #FFB3C6; text-align: center;'>📅 我的運動月曆</h3>", unsafe_allow_html=True)

calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth",
    },
    "initialView": "dayGridMonth",
}

# 顯示日曆
calendar(events=st.session_state['events'], options=calendar_options)

st.markdown("<br><p style='text-align: center; color: #FFB3C6;'>有星星的日子都是進步的證明 🍯</p>", unsafe_allow_html=True)
