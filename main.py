import streamlit as pd
import streamlit as st
import random

# 1. 設置網頁標題與風格
st.set_page_config(page_title="Streamlit 數字解謎王", page_icon="🎲", layout="centered")
st.title("🎲 終極密碼：數字解謎王")
st.write("在 1 到 100 之間猜一個數字，看你幾次之內能猜中！")

# 2. 初始化遊戲狀態 (使用 st.session_state 記憶數據)
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.min_val = 1
    st.session_state.max_val = 100
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []

# 3. 遊戲左側邊欄：顯示當前狀態與成就
with st.sidebar:
    st.header("📊 玩家成就面板")
    st.metric(label="目前猜測次數", value=st.session_state.attempts)
    
    # 趣味稱號系統
    if st.session_state.attempts == 0:
        st.info("🏅 稱號：新手上路")
    elif st.session_state.attempts <= 4 and st.session_state.game_over:
        st.success("👑 稱號：通靈大師！")
    elif st.session_state.attempts <= 8 and st.session_state.game_over:
        st.info("🧠 稱號：邏輯專家")
    elif st.session_state.game_over:
        st.warning("🐌 稱號：非洲酋長")

    # 顯示歷史紀錄
    if st.session_state.history:
        st.subheader("📜 猜測歷史")
        for h in reversed(st.session_state.history):
            st.text(h)

# 4. 遊戲主畫面 UI
st.subheader(f"目前範圍： {st.session_state.min_val}  ～  {st.session_state.max_val}")

# 使用 Form 讓玩家輸入，按下 Enter 或按鈕後才觸發
with st.form(key="guess_form", clear_on_submit=True):
    user_guess = st.number_input(
        "輸入你的預測數字：", 
        min_value=1, 
        max_value=100, 
        step=1,
        disabled=st.session_state.game_over
    )
    submit_button = st.form_submit_button(label="提交答案 🚀")

# 5. 遊戲核心邏輯判斷
if submit_button and not st.session_state.game_over:
    # 檢查是否超出當前提示範圍
    if user_guess < st.session_state.min_val or user_guess > st.session_state.max_val:
        st.warning(f"哎呀！請輸入 {st.session_state.min_val} 到 {st.session_state.max_val} 之間的數字。")
    else:
        st.session_state.attempts += 1
        
        if user_guess == st.session_state.secret_number:
            st.session_state.game_over = True
            st.session_state.history.append(f"第 {st.session_state.attempts} 次：{user_guess} 🎉 答對了！")
            st.balloons() # 噴發慶祝氣球
            st.success(f"🎉 太厲害了！你總共花了 {st.session_state.attempts} 次猜中答案：{st.session_state.secret_number}！")
        elif user_guess < st.session_state.secret_number:
            st.session_state.min_val = user_guess + 1
            st.session_state.history.append(f"第 {st.session_state.attempts} 次：{user_guess} ➡️ 太小了")
            st.error("💡 太小了！再大一點！")
        else:
            st.session_state.max_val = user_guess - 1
            st.session_state.history.append(f"第 {st.session_state.attempts} 次：{user_guess} ➡️ 太大了")
            st.error("💡 太大了！再小一點！")

# 6. 重新開始遊戲按鈕
if st.session_state.game_over:
    if st.button("再玩一局 🔄"):
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.min_val = 1
        st.session_state.max_val = 100
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.history = []
        st.rerun() # 重新整理頁面
