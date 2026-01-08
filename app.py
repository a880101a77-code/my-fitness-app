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
