import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="菡FITNESS GOAL", page_icon="🐾", layout="centered")

# --- 深度自訂 CSS (保持奶茶色) ---
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
    ex_name = st.text_input("運動項目", placeholder="例如：深蹲")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        s = st.number_input("組數", min_value=1, step=1, value=3)
    with c2:
        r = st.number_input("次數", min_value=1, step=1, value=12)
    with c3:
        w = st.number_input("重量(kg)", min_value=0, step=1, value=10)
    
    submitted = st.form_submit_button("打卡存進口袋 🐾")

if submitted:
    date_str = input_date.strftime("%Y-%m-%d")
    st.session_state['workout_data'].append({
        "date": date_str, "exercise": ex_name, "sets": s, "reps": r, "weight": w
    })
    st.snow()
    # 這裡移除 rerun，讓表單自然送出，避免日曆因重新啟動而消失

st.divider()

# --- 3. 運動日曆視圖 ---
# 建立 Event 清單
unique_days = list(set([item['date'] for item in st.session_state['workout_data']]))
calendar_events = [{"title": "🏋️", "start": day, "allDay": True} for day in unique_days]

st.markdown("<h4>🗓️ 菡運動日記</h4>", unsafe_allow_html=True)

calendar_options = {
    "headerToolbar": {"left": "prev,next", "center": "title", "right": "today"},
    "initialView": "dayGridMonth",
    "selectable": True,
    "timeZone": "UTC",
}

# 使用固定的 key 並將日曆放在一個 container 內以提高穩定性
cal_container = st.container()
with cal_container:
    state = calendar(events=calendar_events, options=calendar_options, key="fixed_olaf_calendar")

# --- 4. 點擊邏輯 ---
if state.get("dateClick"):
    clicked_date = state["dateClick"]["date"][:10]
    st.markdown(f"### 🧸 {clicked_date} 的訓練清單")
    
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 20px; border: 2px solid #EAE2D6; margin-bottom: 10px;">
                    <p style="margin:0; color:#8E735B; font-weight:bold;">{item['exercise']}</p>
                    <p style="margin:0; color:#A68A64; font-size: 0.9rem;">{item['sets']} 組 | {item['reps']} 次 | {item['weight']} kg</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 刪除功能
            if st.button(f"🗑️ 移除項目 {idx+1}", key=f"del_{idx}_{clicked_date}"):
                st.session_state['workout_data'].remove(item)
                st.rerun()
    else:
        st.write("這天還沒有小雪球紀錄唷～")

st.markdown("<br><p style='text-align: center; color: #C6AC8F;'>每一小步都是菡的大進步 🍦</p>", unsafe_allow_html=True)
