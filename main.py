import streamlit as st

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

# 5. 主畫面分頁（地圖圖片常駐，無表格）
tab_map, tab_diplomacy = st.tabs(["🗺️ 全疆域戰略地圖 (Military Map)", "🌍 國際外交與戰線 (Diplomacy)"])

# --- TAB 1: 戰略地圖（純圖版） ---
with tab_map:
    st.header("🎯 最高統帥部：疆域守軍臨戰態勢")
    
    # 常駐軍事地圖
    map_url = "https://gamer.com.tw" # 秋海棠地圖源
    st.image("https://bahamut.com.tw", 
             caption="【常駐軍事態勢圖】德械精銳師與機械化部隊已在平津防線、沿海港口集結完畢。", 
             use_container_width=True)
    
    st.subheader("⚔️ 前線總部戰報簡介")
    st.info("💡 **南京首都圈、廣東基地、平津防線及關外邊境** 已佈防超過 95 個滿編主力師，戰備狀態完美，隨時可轉入全面戰略反攻！")

# --- TAB 2: 國際外交與戰線（純圖版） ---
with tab_diplomacy:
    st.header("🌍 遠東與全球國際戰線")
    
    # 常駐國際外交局勢圖
    st.image("https://bahamut.com.tw", 
             caption="【遠東國際外交戰線圖】列強勢力錯綜複雜，我方已全面重塑亞洲與世界新秩序！", 
             use_container_width=True)
    
    st.markdown("---")
    st.subheader("📡 當前外交抉擇與局勢評估")
    
    if not st.session_state.war_declared:
        st.info("💡 歷史評估：我方已全面移除所有歷史枷鎖，百萬精銳德械師隨時可以採取攻勢。")
        if st.button("💥 拒絕對列強妥協：向軸心國與不平等條約宣戰！", type="primary", use_container_width=True):
            st.session_state.war_declared = True
            st.session_state.world_tension = min(100, st.session_state.world_tension + 45)
            st.rerun()
    else:
        st.error("⚔️ 【全面戰爭狀態】我方已對全球帝國主義宣戰！")
        st.markdown("""
        *   **世界緊張度：** 已因我軍爆發反攻行動大幅飆升！
        *   **前線回報：** 移除陸軍腐敗與全 Buff 加成下，全軍組織度上升 **+15%**，後方工廠產能全開。
        *   **國際反應：** 西方列強與鄰國外交關係全面跌入冰點，戰火已無法避免。
        """)
