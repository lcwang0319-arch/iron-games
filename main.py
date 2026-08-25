import streamlit as st
import os

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Streamlit IV: 中華民國崛起", page_icon="🇹🇼", layout="wide")
st.title("🇹🇼 Hearts of Streamlit IV: 中華民國（完全體天警開局）")

# 2. 初始化國家與世界局勢狀態
if "game_date" not in st.session_state:
    st.session_state.game_date = {"year": 1936, "month": 1, "day": 1}
    st.session_state.country = "中華民國 (Republic of China)"
    
    # 核心資源 (全 Buff 狀態)
    st.session_state.political_power = 500  
    st.session_state.stability = 100         
    st.session_state.war_support = 100       
    st.session_state.manpower = 50000000     
    st.session_state.civ_factories = 80     
    st.session_state.mil_factories = 60     
    
    # 🎮 新增：世界緊張度與戰爭事件狀態
    st.session_state.world_tension = 0  # 世界緊張度 %
    st.session_state.war_declared = False # 是否宣戰
    st.session_state.event_trigger = False # 是否觸發事件彈窗
    
    st.session_state.active_buffs = [
        "✅ 移除【陸軍腐敗】：陸軍組織度 +20%",
        "✅ 移除【財政崩潰】：民用工廠建造速度 +30%",
        "✅ 啟動【四億同胞】：核心人力增長 +5.00%",
        "✅ 啟動【工業大躍進】：工廠產出 +25%"
    ]

# 3. 頂部資源列 (HUD) + 世界緊張度
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
    # 鋼鐵雄心核心：火球圖示的世界緊張度
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
        
        # 隨著時間隨機增加一點世界緊張度
        if st.session_state.world_tension < 100:
            st.session_state.world_tension += min(100, round(0.2, 1))
            
        st.rerun()

    st.markdown("---")
    st.header("🔰 當前國家精神")
    for buff in st.session_state.active_buffs:
        st.caption(buff)

# 5. 核心重大外交事件（圖片彈窗區）
if st.session_state.event_trigger:
    # 建立一個極具儀式感的鋼鐵雄心式大宣告框
    st.error("🚨 【重大國際歷史事件：全面宣戰！】")
    
    # 🖼️ 核心：顯示圖片邏輯 (優先讀取本地圖片，若無則用網路備用圖片)
    img_path = "world_war.png"
    backup_url = "https://unsplash.com" # 復古戰爭感底圖
    
    if os.path.exists(img_path):
        st.image(img_path, caption="《泰晤士報》頭版：遠東雄獅覺醒，震驚歐美列強！", use_container_width=True)
    else:
        st.image(backup_url, caption="【國際戰線圖】中華民國正式拒絕承認帝國主義不平等條約，大軍開拔！", use_container_width=True)
        
    st.markdown("""
    ### 🔔 號外！中華民國最高統帥部發表對全球宣戰佈告！
    因應國際局勢波譎雲詭，我方已全面解除所有歷史枷鎖。
    百萬精銳德械師、機械化部隊已在邊境集結完畢，目標：徹底收復所有失去的國土，重塑亞洲與世界新秩序！
    
    *   **世界緊張度 飆升 +45%**
    *   **全軍組織度 上升 +15%**
    *   **西方列強外交關係 跌入冰點**
    """)
    if st.button("知道了，不惜一切代價贏得勝利！ 🇹🇼"):
        st.session_state.event_trigger = False
        st.rerun()
    st.markdown("---")

# 6. 主畫面分頁
tab_map, tab_diplomacy = st.tabs(["🗺️ 全疆域戰略地圖", "🌍 國際外交戰線"])

with tab_map:
    st.header("守軍與前線狀態")
    map_data = {
        "行省 / 地區": ["南京 (首都圈)", "廣東 (南方基地)", "平津防線 (抗日最前線)", "東北邊境 (關外)"],
        "駐防精銳師團數": ["30 個機械化步兵師", "15 個常備師", "40 個德械師 (全裝)", "等待下達進攻命令的 50 個主力師"],
        "戰備狀態": ["優良", "優良", "完美 (隨時可發動反攻)", "全面臨戰"]
    }
    st.table(map_data)

with tab_diplomacy:
    st.header("🌍 國際外交與宣戰抉擇")
    st.write("目前世界各國正緊盯著你的每一步動作。")
    
    # 宣戰按鈕
    if not st.session_state.war_declared:
        if st.button("💥 拒絕對列強妥協：向軸心國與不平等條約宣戰！", type="primary", use_container_width=True):
            st.session_state.war_declared = True
            st.session_state.event_trigger = True # 觸發上面的圖片與事件公告
            st.session_state.world_tension = min(100, st.session_state.world_tension + 45)
            st.rerun()
    else:
        st.success("⚔️ 目前正處於【大東亞與全球解放戰爭】狀態！")
