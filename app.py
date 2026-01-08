import streamlit as st
from datetime import datetime
from streamlit_calendar import calendar

# --- 1. 頁面設定 ---
st.set_page_config(page_title="菡FITNESS GOAL", page_icon="🐾", layout="centered")

# --- 2. 深度自訂 CSS ---
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
    .fc-event { background-color: #C6AC8F !important; border: none !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🍦 菡FITNESS GOAL 🍦</h1>", unsafe_allow_html=True)

# --- 3. 初始化資料 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 4. 紀錄表單 ---
with st.form(key="olaf_workout_form", clear_on_submit=True):
    st.markdown("### 🍪 訓練紀錄")
    input_date = st.date_input("訓練日期", datetime.now())
    
    workout_type = st.radio("訓練類型", ["重量訓練", "有氧運動"], horizontal=True)
    ex_name = st.text_input("運動項目", placeholder="例如：深蹲 / 跑步機")
    
    # 預設數據
    s, w, duration = 0, 0, 0
    
    # --- 動態顯示邏輯 ---
    if workout_type == "重量訓練":
        col1, col2 = st.columns(2)
        with col1:
            s = st.number_input("組數", min_value=1, step=1, value=3)
        with col2:
            w = st.number_input("重量 (kg)", min_value=0, step=1, value=10)
    else:
        # 有氧模式：隱藏組數重量，顯示分鐘
        duration = st.number_input("運動多久呢？ (單位：分鐘)", min_value=1, step=1, value=30)
    
    submitted = st.form_submit_button("打卡存進口袋 🐾")

# --- 5. 處理表單送出 ---
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

# --- 6. 運動日曆 ---
st.markdown("<h4>🗓️ 菡運動日記</h4>", unsafe_allow_html=True)

calendar_events = []
for item in st.session_state['workout_data']:
    icon = "⏱️" if item["type"] == "有氧運動" else "💪"
    calendar_events.append({
        "title": f"{icon} {item['exercise']}", 
        "start": item["date"], 
        "allDay": True
    })

calendar_options = {
    "headerToolbar": {"left": "prev,next today", "center": "title", "right": ""},
    "initialView": "dayGridMonth",
    "selectable": True,
    "timeZone": "local",
}

cal_state = calendar(events=calendar_events, options=calendar_options, key="workout_calendar_v4")

# --- 7. 點擊詳情顯示 ---
if cal_state.get("dateClick"):
    clicked_date = cal_state["dateClick"]["date"][:10]
    st.markdown(f"### 🧸 {clicked_date} 的訓練清單")
    
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            # 取得變數
            ex = item['exercise']
            tp = item['type']
            
            # --- 核心邏輯：判斷顯示文字 ---
            if tp == "有氧運動":
                # 明確加上「分鐘」
                info_text = f"⏱️ 運動時長：{int(item['duration'])} 分鐘"
            else:
                # 明確加上「組數」與「kg」
                info_text = f"💪 {int(item['sets'])} 組 | {item['weight']} kg"
            
            st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 20px; border: 2px solid #EAE2D6; margin-bottom: 10px;">
                    <p style="margin:0; color:#8E735B; font-weight:bold;">{ex} <small>({tp})</small></p>
                    <p style="margin:0; color:#A68A64; font-size: 0.9rem;">{info_text}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ 移除項目 {idx+1}", key=f"del_{idx}_{clicked_date}"):
                st.session_state['workout_data'].remove(item)
                st.rerun()
    else:
        st.write("這天還沒有紀錄唷～")

st.markdown("<br><p style='text-align: center; color: #C6AC8F;'>每一小步都是菡的大進步 🍦</p>", unsafe_allow_html=True)
