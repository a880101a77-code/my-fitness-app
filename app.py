import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="小熊健身日誌", page_icon="🏋️", layout="centered")

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
    .fc-event { background-color: #FFB3C6 !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏋️ 健身小日常 🏋️</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料儲存 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 2. 紀錄表單 ---
with st.form(key="workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 紀錄新訓練</h3>", unsafe_allow_html=True)
    # 這裡確保存入的是 YYYY-MM-DD 字串
    d = st.date_input("訓練日期", datetime.now())
    ex_name = st.text_input("運動項目", placeholder="例如：臥推")
    col1, col2 = st.columns(2)
    with col1:
        s = st.number_input("組數", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("次數/重量", min_value=1, step=1, value=12)
    
    submitted = st.form_submit_button("送出紀錄 🐾")

if submitted:
    # 強制將日期轉換為純字串，不帶任何時間資訊
    date_str = d.strftime("%Y-%m-%d")
    st.session_state['workout_data'].append({
        "date": date_str,
        "exercise": ex_name,
        "sets": s,
        "reps": r
    })
    st.balloons()

st.divider()

# --- 3. 運動日曆視圖 ---
# 確保 event 裡的日期也是純字串
unique_days = list(set([item['date'] for item in st.session_state['workout_data']]))
calendar_events = [{"title": "🏋️", "start": day, "allDay": True} for day in unique_days]

st.markdown("<h3 style='color: #FFB3C6; text-align: center;'>📅 運動月曆</h3>", unsafe_allow_html=True)

calendar_options = {
    "headerToolbar": {"left": "today prev,next", "center": "title", "right": ""},
    "initialView": "dayGridMonth",
    "selectable": True,
    "timeZone": "UTC", # 強制日曆元件使用 UTC，不要自動轉換本地時區
}

state = calendar(events=calendar_events, options=calendar_options, key="my_calendar")

# --- 4. 點擊邏輯：終極字串切片法 ---
if state.get("dateClick"):
    # 直接從點擊資訊中切出前 10 個字元 (YYYY-MM-DD)
    # 不管它是 2026-01-08T00:00... 還是什麼，我們只要前十位
    clicked_date = state["dateClick"]["date"][:10]
    
    st.markdown(f"### 🗓️ {clicked_date} 的訓練清單")
    
    # 用純字串比對
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            with st.container():
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 20px; border: 2px solid #FFE5EC; margin-bottom: 10px;">
                    <p style="margin:0; color:#FF85A2; font-weight:bold; font-size:1.1rem;">{item['exercise']}</p>
                    <p style="margin:0; color:#4A4A4A;">{item['sets']} 組 | {item['reps']} 次/公斤</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ 刪除這筆項目", key=f"del_{idx}_{clicked_date}"):
                    st.session_state['workout_data'].remove(item)
                    st.rerun()
    else:
        st.write("✨ 這天還空空的，來場訓練吧！")

st.markdown("<br><p style='text-align: center; color: #FFB3C6;'>每一刻的汗水都值得被紀錄 🍯</p>", unsafe_allow_html=True)
