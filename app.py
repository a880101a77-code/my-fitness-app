import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="菡FITNESS GOAL", page_icon="🐾", layout="centered")

# --- 深度自訂 CSS ---
st.markdown("""
    <style>
    .main { background-color: #F3E9DC; }
    h1, h3, h4 { color: #8E735B !important; font-family: "Microsoft JhengHei", sans-serif; text-align: center; }
    p { color: #A68A64; }
    .stForm { 
        border: 2px solid #DDBEAA !important; 
        border-radius: 25px !important; 
        background-color: #FFFFFF !important; 
        padding: 20px !important;
    }
    .stButton>button { 
        background-color: #C6AC8F; color: white; border-radius: 20px; 
        border: none; font-weight: bold; transition: 0.3s; width: 100%;
    }
    .stButton>button:hover { background-color: #8E735B; color: white; }
    
    .fc-header-toolbar { color: #8E735B; }
    .fc-daygrid-day-number { color: #8E735B !important; text-decoration: none !important; }
    .fc-day-today { background-color: #EAE2D6 !important; }
    .fc-event { background-color: #C6AC8F !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🍦 菡FITNESS GOAL 🍦</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 2. 紀錄表單 ---
with st.form(key="olaf_workout_form", clear_on_submit=True):
    st.markdown("### 🍪 訓練紀錄")
    input_date = st.date_input("訓練日期", datetime.now())
    
    workout_type = st.radio("訓練類型", ["重量訓練", "有氧運動"], horizontal=True)
    ex_name = st.text_input("運動項目", placeholder="例如：深蹲 / 跑步機")
    
    # 初始化數據
    s, w, duration = 0, 0, 0
    
    if workout_type == "重量訓練":
        col1, col2 = st.columns(2)
        with col1:
            s = st.number_input("組數", min_value=1, step=1, value=3)
        with col2:
            w = st.number_input("重量(kg)", min_value=0, step=1, value=10)
    else:
        # 這裡縮排必須正確
        duration = st.number_input("運動時長 (分鐘)", min_value=1, step=1, value=30)
    
    submitted = st.form_submit_button("打卡存進口袋 🐾")

# --- 3. 處理表單送出 ---
if submitted:
    date_str = input_date.strftime("%Y-%m-%d")
    new_record = {
        "date": date_str, 
        "type": workout_type,
        "exercise": ex_name,
        "sets": s if workout_type == "重量訓練" else None,
        "weight": w if workout_type == "重量訓練" else None,
        "duration": duration if workout_type == "有氧運動" else None
    }
    st.session_state['workout_data'].append(new_record)
    st.snow()
    st.success(f"已記錄 {ex_name}！")

st.divider()

# --- 4. 運動日曆視圖 ---
calendar_events = []
for item in st.session_state['workout_data']:
    icon = "⏱️" if item["type"] == "有氧運動" else "💪"
    calendar_events.append({"title": icon, "start": item["date"], "allDay": True})

st.markdown("<h4>🗓️ 菡運動日記</h4>", unsafe_allow_html=True)

calendar_options = {
    "headerToolbar": {"left": "prev,next", "center": "title", "right": "today"},
    "initialView": "dayGridMonth",
    "selectable": True,
    "timeZone": "UTC",
}

cal_container = st.container()
with cal_container:
    state = calendar(events=calendar_events, options=calendar_options, key="fixed_olaf_calendar")

# --- 5. 點擊詳情顯示 ---
if state.get("dateClick"):
    clicked_date = state["dateClick"]["date"][:10]
    st.markdown(f"### 🧸 {clicked_date} 的訓練清單")
    
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
