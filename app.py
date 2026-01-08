import streamlit as st
from datetime import datetime

st.title("💪 我的健身訓練日誌")

with st.form("workout_form"):
    date = st.date_input("選擇健身日期", datetime.now())
    exercise = st.text_input("運動項目 (例如：臥推)")
    sets = st.number_input("組數", min_value=1, step=1)
    reps = st.number_input("每組次數", min_value=1, step=1)
    submitted = st.form_submit_button("儲存紀錄")

if submitted:
    st.success(f"已紀錄：{date} - {exercise} {sets}組 x {reps}下")
    st.balloons()
import streamlit as st
from datetime import datetime

# --- 頁面設定：可愛簡約風 ---
st.set_page_config(page_title="小熊健身日誌", page_icon="🧸", layout="centered")

# 使用 CSS 打造可愛感 (粉嫩色系、大圓角、手寫感字體)
st.markdown("""
    <style>
    .main {
        background-color: #FFF9FB; /* 極淺粉色背景 */
    }
    h1 {
        color: #FF85A2; /* 莓果粉 */
        font-family: "Microsoft JhengHei", sans-serif;
        text-align: center;
        font-size: 2.5rem;
    }
    .stButton>button {
        background-color: #FFB3C6; /* 粉紅鈕扣 */
        color: white;
        border: none;
        border-radius: 20px; /* 超圓角 */
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF85A2;
        border: none;
        color: white;
    }
    /* 卡片樣式 */
    .css-1r6slb0, .stForm {
        border: 2px solid #FFE5EC !important;
        border-radius: 25px !important;
        background-color: white !important;
        padding: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- App 標題 ---
st.markdown("<h1>☁️ 健身小日常 ☁️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0A0A0;'>今天也辛苦了！動一動身體吧 ✨</p>", unsafe_allow_html=True)

# --- 主要表單 ---
with st.form("workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 紀錄訓練</h3>", unsafe_allow_html=True)
    
    # 日期選擇
    d = st.date_input("今天日期是？", datetime.now())
    
    # 運動項目
    ex_name = st.text_input("做了什麼運動呢？", placeholder="例如：開合跳、伸展...")
    
    col1, col2 = st.columns(2)
    with col1:
        s = st.number_input("做了幾組？", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("每組幾次/公斤？", min_value=1, step=1, value=12)
    
    submitted = st.form_submit_button("打卡完成紀錄 🐾")

# --- 儲存後顯示 ---
if submitted:
    st.balloons() # 噴出氣球慶祝
    st.markdown(f"""
        <div style="background-color: #FFE5EC; padding: 15px; border-radius: 20px; text-align: center;">
            <p style="color: #FF85A2; font-size: 1.2rem; font-weight: bold; margin: 0;">🌷 紀錄成功囉！</p>
            <p style="color: #4A4A4A; margin: 5px 0;">{d} | {ex_name} | {s}組 x {r}次</p>
        </div>
    """, unsafe_allow_html=True)

# --- 下方裝飾 ---
st.markdown("<br><p style='text-align: center; color: #FFB3C6;'>加油！離目標又進了一步 🍯</p>", unsafe_allow_html=True)
