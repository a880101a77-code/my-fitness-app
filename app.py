import streamlit as st
from datetime import datetime
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
    /* 強制修改日曆事件樣式為槓鈴感 */
    .fc-event-title { font-weight: bold !important; }
    .fc-event { background-color: #FFB3C6 !important; border: none !important; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏋️ 健身小日常 🏋️</h1>", unsafe_allow_html=True)

# --- 1. 初始化資料儲存 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = [] # 儲存完整的運動細節

# --- 2. 快速打卡表單 ---
with st.form(key="workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 紀錄新訓練</h3>", unsafe_allow_html=True)
    d = st.date_input("訓練日期", datetime.now())
    ex_name = st.text_input("運動項目", placeholder="例如：臥推")
    col1, col2 = st.columns(2)
    with col1:
        s = st.number_input("組數", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("次數/重量", min_value=1, step=1, value=12)
    
    submitted = st.form_submit_button("送出紀錄 🐾")

if submitted:
    # 儲存數據
    st.session_state['workout_data'].append({
        "date": d.isoformat(),
        "exercise": ex_name,
        "sets": s,
        "reps": r
    })
    st.balloons()

st.divider()

# --- 3. 準備日曆事件 (將所有運動合併為一個槓鈴圖示) ---
# 我們讓每一天只要有運動，就顯示一個「🏋️」
unique_days = list(set([item['date'] for item in st.session_state['workout_data']]))
calendar_events = [
    {"title": "🏋️ 有運動!", "start": day, "allDay": True} for day in unique_days
]

# --- 4. 運動日曆視圖 ---
st.markdown("<h3 style='color: #FFB3C6; text-align: center;'>📅 運動月曆</h3>", unsafe_allow_html=True)
st.info("💡 點擊下方日曆的日期，可以查看當天的詳細訓練內容喔！")

calendar_options = {
    "headerToolbar": {"left": "today prev,next", "center": "title", "right": ""},
    "initialView": "dayGridMonth",
    "selectable": True,
}

# 顯示日曆並捕捉點擊動作
state = calendar(events=calendar_events, options=calendar_options, key="my_calendar")

# --- 5. 點擊日曆後的詳細內容顯示 ---
if state.get("dateClick"):
    clicked_date = state["dateClick"]["date"].split("T")[0]
    st.markdown(f"### 🗓️ {clicked_date} 的訓練清單")
    
    # 過濾出當天的運動
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            with st.expander(f"項目 {idx+1}: {item['exercise']}"):
                st.write(f"💪 組數: {item['sets']} 組")
                st.write(f"🔢 次數/重量: {item['reps']}")
                if st.button(f"刪除這筆 (項目 {idx+1})", key=f"del_{idx}"):
                    st.session_state['workout_data'].remove(item)
                    st.rerun()
    else:
        st.write("這天還沒紀錄運動喔～加油！")

st.markdown("<br><p style='text-align: center; color: #FFB3C6;'>每一刻的汗水都值得被紀錄 🍯</p>", unsafe_allow_html=True)
