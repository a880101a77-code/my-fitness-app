import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# --- 頁面設定 ---
st.set_page_config(page_title="歐拉夫健身日誌", page_icon="🐾", layout="centered")

# --- 奶茶色 & 歐拉夫主題 CSS ---
st.markdown("""
    <style>
    .main { 
        background-color: #F3E9DC; /* 暖奶茶底色 */
    }
    h1 { 
        color: #8E735B; /* 深奶茶色文字 */
        font-family: "Microsoft JhengHei", sans-serif; 
        text-align: center; 
    }
    .stButton>button { 
        background-color: #C6AC8F; /* 奶茶棕按鈕 */
        color: white; 
        border-radius: 25px; 
        width: 100%; 
        border: none; 
        font-weight: bold;
        height: 3em;
    }
    .stForm { 
        border: 3px solid #EAE2D6 !important; 
        border-radius: 30px !important; 
        background-color: #FFFFFF !important; 
        padding: 25px !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    /* 日曆標籤顏色 */
    .fc-event { 
        background-color: #C6AC8F !important; 
        border: none !important; 
        cursor: pointer; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 標題區 ---
st.markdown("<h1>🍦 歐拉夫動一動 🍦</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A68A64;'>今天也要像歐拉夫一樣放鬆又健康唷～</p>", unsafe_allow_html=True)

# --- 1. 初始化資料儲存 ---
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = []

# --- 2. 紀錄表單 ---
with st.form(key="olaf_workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #8E735B;'>🍪 訓練紀錄</h3>", unsafe_allow_html=True)
    
    input_date = st.date_input("訓練日期", datetime.now())
    ex_name = st.text_input("運動項目", placeholder="例如：慢跑、舉重...")
    
    # 三欄並排：組數、次數、重量
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
        "date": date_str,
        "exercise": ex_name,
        "sets": s,
        "reps": r,
        "weight": w
    })
    st.snow() # 歐拉夫主題適合噴雪花！
    st.success(f"成功幫歐拉夫記下來了！")

st.divider()

# --- 3. 運動日曆視圖 ---
unique_days = list(set([item['date'] for item in st.session_state['workout_data']]))
calendar_events = [{"title": "🍦", "start": day, "allDay": True} for day in unique_days]

st.markdown("<h4 style='color: #8E735B; text-align: center;'>🗓️ 歐拉夫運動地圖</h4>", unsafe_allow_html=True)

calendar_options = {
    "headerToolbar": {"left": "today prev,next", "center": "title", "right": ""},
    "initialView": "dayGridMonth",
    "selectable": True,
}

state = calendar(events=calendar_events, options=calendar_options, key="olaf_calendar")

# --- 4. 點擊邏輯：解決日期偏移 ---
if state.get("dateClick"):
    # 暴力修正日期字串
    raw_date = state["dateClick"]["date"]
    if "T" in raw_date:
        # 轉成時間物件並加 12 小時抵消時區偏誤
        dt = datetime.strptime(raw_date.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
        fixed_dt = dt + timedelta(hours=12)
        clicked_date = fixed_dt.strftime("%Y-%m-%d")
    else:
        clicked_date = raw_date[:10]
    
    st.markdown(f"### 🧸 {clicked_date} 的訓練清單")
    
    todays_workouts = [item for item in st.session_state['workout_data'] if item['date'] == clicked_date]
    
    if todays_workouts:
        for idx, item in enumerate(todays_workouts):
            with st.container():
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 20px; border: 2px solid #EAE2D6; margin-bottom: 10px;">
                    <p style="margin:0; color:#8E735B; font-weight:bold;">{item['exercise']}</p>
                    <p style="margin:0; color:#A68A64; font-size: 0.9rem;">{item['sets']} 組 | {item['reps']} 次 | {item['weight']} kg</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ 移除", key=f"del_{idx}_{clicked_date}"):
                    st.session_state['workout_data'].remove(item)
                    st.rerun()
    else:
        st.write("這天還沒有小雪球紀錄唷～")

st.markdown("<br><p style='text-align: center; color: #C6AC8F;'>每一小步都是歐拉夫的大進步 🍦</p>", unsafe_allow_html=True)
