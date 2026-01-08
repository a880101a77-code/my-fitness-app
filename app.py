import streamlit as st
from datetime import datetime

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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>☁️ 健身小日常 ☁️</h1>", unsafe_allow_html=True)

# --- 核心表單 (這裡我們確保 key 是唯一的) ---
with st.form(key="unique_workout_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #FFB3C6;'>🎀 紀錄訓練</h3>", unsafe_allow_html=True)
    
    d = st.date_input("今天日期是？", datetime.now())
    ex_name = st.text_input("做了什麼運動呢？", placeholder="例如：開合跳...")
    
    col1, col2 = st.columns(2)
    with col1:
        s = st.number_input("做了幾組？", min_value=1, step=1, value=3)
    with col2:
        r = st.number_input("每組幾次/公斤？", min_value=1, step=1, value=12)
    
    submitted = st.form_submit_button("打卡完成紀錄 🐾")

if submitted:
    st.balloons()
    st.success(f"🌷 紀錄成功：{d} {ex_name}")

st.markdown("<br><p style='text-align: center; color: #FFB3C6;'>加油！離目標又進了一步 🍯</p>", unsafe_allow_html=True)
