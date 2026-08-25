import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Streamlit IV: 中華民國崛起", page_icon="🇹🇼", layout="wide")
st.title("🇹🇼 Hearts of Streamlit IV: 中華民國（完全體天警開局）")

# 2. 安全的防禦性初始化
if "game_date" not in st.session_state:
    st.session_state.game_date = {"year": 1936, "month": 1, "day": 1}
if "country" not in st.session_state:
    st.session_state.country = "中華民國 (Republic of China)"
if "political_power" not in st.session_state:
    st.session_state.political_power = 500  
if "stability" not in st.session_state:
    st.session_state.stability = 100         
if "war_support" not in st.session_state:
    st.session_state.war_support = 100       
if "manpower" not in st.session_state:
    st.session_state.manpower = 50000000     
if "civ_factories" not in st.session_state:
    st.session_state.civ_factories = 80     
if "mil_factories" not in st.session_state:
    st.session_state.mil_factories = 60     
if "world_tension" not in st.session_state:
    st.session_state.world_tension = 0  
if "war_declared" not in st.session_state:
    st.session_state.war_declared = False 
if "active_buffs" not in st.session_state:
    st.session_state.active_buffs = [
        "✅ 移除【陸軍腐敗】：陸軍組織度 +20%",
        "✅ 移除【財政崩潰】：民用工廠建造速度 +30%",
        "✅ 啟動【四億同胞】：核心人力增長 +5.00%",
        "✅ 啟動【工業大躍進】：工廠產出 +25%"
    ]

# 3. 頂部資源列 (HUD)
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.metric("📅 遊戲日期", f"{st.session_state.game_date['year']}-{st.session_state.game_date['month']:02d}-{st.session_state.game_date['day']:02d}")
with col2:
    st.metric("👑 政治點數 (PP)", f"{st.session_state.political_power}")
with col3:
    st.metric("⚖️ 穩定度", f"{st.session_state.stability}%")
with col4:
    st.metric("🔥 戰爭支持度", f"{st.session_state.war_support}%")
with col5:
    st.metric("👥 可用人力", f"{st.session_state.manpower:,}")
with col6:
    st.metric("🏭 工廠", f"{st.session_state.civ_factories} / {st.session_state.mil_factories}")
with col7:
    st.metric("🔥 世界緊張度", f"{st.session_state.world_tension}%")

st.markdown("---")

# 4. 側邊欄：控制台
with st.sidebar:
    st.header("⏱️ 時間與戰略控制")
    if st.button("▶️ 推進下一天 (Next Day)", use_container_width=True):
        st.session_state.game_date["day"] += 1
        if st.session_state.game_date["day"] > 30:
            st.session_state.game_date["day"] = 1
            st.session_state.game_date["month"] += 1
            if st.session_state.game_date["month"] > 12:
                st.session_state.game_date["month"] = 1
                st.session_state.game_date["year"] += 1
        if st.session_state.world_tension < 100:
            st.session_state.world_tension = min(100, st.session_state.world_tension + 1)
        st.rerun()

    if st.button("🔄 重設全域數據", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.header("🔰 當前國家精神")
    for buff in st.session_state.active_buffs:
        st.caption(buff)

# 5. 主畫面分頁
tab_map, tab_diplomacy = st.tabs(["🗺️ 全疆域戰略地圖 (Military Map)", "🌍 國際外交與戰線 (Diplomacy)"])

# --- TAB 1: 戰略地圖（使用 Python Matplotlib 強制渲染，100%能看見） ---
with tab_map:
    st.header("🎯 最高統帥部：疆域守軍軍事地圖")
    
    # 用程式碼畫一個秋海棠疆域的示意圖與防線
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    
    # 模擬畫一個中華民國秋海棠形狀的區塊
    t = np.linspace(0, 2*np.pi, 100)
    # 核心疆域波形
    x = 12 * np.cos(t) + 3 * np.sin(2*t) + 100
    y = 8 * np.sin(t) + 2 * np.cos(3*t) + 35
    
    # 填滿國家範圍（藍色代表中華民國核心勢力範圍）
    ax.fill(x, y, color='#003399', alpha=0.6, label='ROC Core Territory (秋海棠疆域)')
    
    # 畫出核心防線點（南京、平津、廣東、關外）
    defense_x = [118, 116, 113, 123]
    defense_y = [32, 39, 23, 41]
    defense_names = ['Nanjing', 'Pingjin', 'Guangdong', 'Guanwai']
    ax.scatter(defense_x, defense_y, color='#ff0000', s=150, zorder=5, label=' 精銳德械師駐防要塞')
    
    for i, txt in enumerate(defense_names):
        ax.annotate(txt, (defense_x[i]+0.5, defense_y[i]+0.5), color='white', fontsize=12, weight='bold')

    # 若全面宣戰，畫出戰線推進箭頭
    if st.session_state.war_declared:
        ax.arrow(116, 39, 5, 5, head_width=1.5, head_length=2, fc='#ff3333', ec='#ff3333', label='戰線全線反攻推進中')
        ax.arrow(123, 41, 4, -2, head_width=1.5, head_length=2, fc='#ff3333', ec='#ff3333')
    
    ax.set_title("Republic of China - Theater Strategy Map", color='white', fontsize=16, weight='bold')
    ax.grid(True, color='#333333', linestyle='--')
    ax.tick_params(colors='white')
    ax.legend(loc='lower left', facecolor='#222222', edgecolor='white', labelcolor='white')
    
    # 渲染至 Streamlit 網頁
    st.pyplot(fig)
    
    st.info("💡 **目前戰報：** 畫面上紅色核心要塞（南京、平津、廣東及關外防線）已佈防超過 95 個滿編德械主力師，戰備狀態完美。")

# --- TAB 2: 國際外交與戰線（使用雷達局勢圖強制渲染，100%能看見） ---
with tab_diplomacy:
    st.header("🌍 遠東與全球國際外交戰線")
    
    # 用 Matplotlib 畫一個國際關係雷達角力圖
    labels = np.array(['Stability', 'War Support', 'Industry', 'Manpower', 'Army Strength'])
    stats = np.array([st.session_state.stability, st.session_state.war_support, 85, 95, 90])
    
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    stats = np.concatenate((stats, [stats[0]]))
    angles += angles[:1]
    
    fig_radar, ax_radar = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor='#1e1e1e')
    ax_radar.set_facecolor('#111111')
    
    ax_radar.fill(angles, stats, color='#ffcc00', alpha=0.4, label='中華民國實力雷達')
    ax_radar.plot(angles, stats, color='#ffcc00', linewidth=2)
    
    ax_radar.set_thetagrids(np.degrees(angles[:-1]), labels, color='white', fontsize=12, weight='bold')
    ax_radar.set_rgrids([20, 40, 60, 80, 100], labels=[], color='#444444')
    ax_radar.tick_params(colors='white')
    ax_radar.set_title("Global Geopolitical Influence Radar", color='white', fontsize=14, weight='bold', pad=20)
    
    st.pyplot(fig_radar)
    
    st.markdown("---")
    st.subheader("📡 當前外交抉擇與局勢評估")
    
    if not st.session_state.war_declared:
        st.info("💡 歷史評估：我方已全面移除所有歷史枷鎖，隨時可以拒絕承認列強不平等條約。")
        if st.button("💥 拒絕對列強妥協：向軸心國與不平等條約宣戰！", type="primary", use_container_width=True):
            st.session_state.war_declared = True
            st.session_state.world_tension = min(100, st.session_state.world_tension + 45)
            st.rerun()
    else:
        st.error("⚔️ 【全面戰爭狀態】我方已對全球帝國主義宣戰！")
        st.markdown("""
        *   **地圖更新：** 戰略大圖上已出現紅色「**戰線全線反攻推進中**」的突擊箭頭！
        *   **前線回報：** 在全 Buff 加成下，全軍組織度大幅上升，後方工廠產能全開。
        *   **國際反應：** 列強外交關係全面跌入冰點，全面反攻戰役打響。
        """)
