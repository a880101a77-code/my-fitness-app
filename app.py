import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="Fitness goal", page_icon="🏋️", layout="centered")

# --- 可愛風格 CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFF9FB; }
    h1 { color: #FF85A2; font-family: "Microsoft JhengHei", sans-serif; text-align: center; }
    .stButton>button { 
        background-color: #FFB3C6; color: white; border-radius: 20px; 
        width: 100%; border: none; font-weight: bold;
    }
    .stForm { border: 2px solid #FFE5EC !important; border-radius: 25px !important; background-color: white !important; padding: 20px !important; }
    .fc-event { background-color: #FFB3C6 !important; border: none !important; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏋️ 健身小日常 🏋️</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料儲存 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 2. 紀錄表單 ---
with st.form(key="workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 紀錄新訓練</h3>", unsafe_allow_html=True)
    
    d = st.date_input("訓練日期", datetime.now())
    ex_name = st.text_input("運動項目", placeholder="例如：臥推")
    
    # 這裡修正了欄位定義，改成三個欄位：組數、次數、重量
    col1, col2, col3 = st.columns(3)
    with col1:
        s = st.number_input("組數", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("次數", min_value=1, step=1, value=15)
    with col3:
        w = st.number_input("重量(kg)", min_value=0, step=1, value=200)
    
    submitted = st.form_submit_button("送出紀錄 🐾")

if submitted:
    date_str = d.strftime("%Y-%m-%d")
    st.session_state['workout_data'].append({
        "date": date_str,
        "exercise": ex_name,
        "sets": s,
        "reps": r,
        "weight": w
    })
    st.balloons()

st.divider()

# --- 3. 運動日曆視圖 ---
unique_days = list(set([item['date'] for item in st.session_state['workout_data']]))
calendar_events = [{"title": "🏋️", "start": day, "allDay": True} for day in unique_days]

st.markdown("<h3 style='color: #FFB3C6; text-align: center;'>📅 運動月曆</h3>", unsafe_allow_html=True)

calendar_options = {
    "headerToolbar": {"left": "today prev,next", "center": "title", "right": ""},
    "initialView": "dayGridMonth",
    "selectable": True,
}

state = calendar(events=calendar_events, options=calendar_options, key="my_calendar")

# --- 4. 點擊邏輯：解決日期偏移 ---
if state.get("dateClick"):
    # 獲取原始字串
    raw_date = state["dateClick"]["date"]
    
    # 修正邏輯：如果字串包含 T00:00，通常會因為時區偏移被當成前一天
    # 我們將其轉為物件後加 12 小時，確保它留在正確的那天
    if "T" in raw_date:
        temp_dt = datetime.strptime(raw_date.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
        fixed_dt = temp_dt + timedelta(hours=12)
        clicked_date = fixed_dt.strftime("%Y-%m-%d")
    else:
        clicked_date = raw_date[:10]
    
    st.markdown(f"### 🗓️ {clicked_date} 的訓練清單")
    
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            with st.container():
                # 這裡加入了「重量」的顯示
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 20px; border: 2px solid #FFE5EC; margin-bottom: 10px;">
                    <p style="margin:0; color:#FF85A2; font-weight:bold; font-size:1.1rem;">{item['exercise']}</p>
                    <p style="margin:0; color:#4A4A4A;">{item['sets']} 組 | {item['reps']} 次 | {item.get('weight', 0)} kg</p>
                </div>
                """, unsafe_allow_html
