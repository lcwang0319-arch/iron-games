import streamlit as st
import random

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Streamlit IV: 中華民國崛起", page_icon="🇹🇼", layout="wide")
st.title("🇹🇼 Hearts of Streamlit IV: 中華民國（完全體天警開局）")

# 2. 初始化國家狀態 (修改為中華民國，且關閉 Debuff、開啟頂級 Buff)
if "game_date" not in st.session_state:
    st.session_state.game_date = {"year": 1936, "month": 1, "day": 1}
    st.session_state.country = "中華民國 (Republic of China)"
    
    # ─── 核心國家資源 (1:1 復刻 HoI4 數值，但經過 Buff 強化) ───
    st.session_state.political_power = 500  # 政治點數：開局大量滿溢
    st.session_state.stability = 100         # 穩定度：% (移除原本的動盪)
    st.session_state.war_support = 100       # 戰爭支持度：% (全國萬眾一心)
    st.session_state.manpower = 50000000     # 可用人力：高達 5000 萬的恐怖核心人力
    
    # ─── 工業體制 (全開 Buff) ───
    st.session_state.civ_factories = 80     # 民用工廠 (直接超越原版列強)
    st.session_state.mil_factories = 60     # 軍用工廠
    
    # ─── 軍備生產線 ───
    st.session_state.infantry_equipment = 50000  # 步兵裝備庫存
    st.session_state.artillery = 5000            # 火砲庫存
    st.session_state.assigned_mil_inf = 20       # 分配給步兵裝備
    st.session_state.assigned_mil_art = 20       # 分配給火砲
    
    # ─── 國策與 Buff 狀態 ───
    st.session_state.current_focus = "無"
    st.session_state.focus_progress = 0
    st.session_state.completed_focuses = []
    
    # ─── 移除所有原本的 Debuff，直接啟動最強民族 Buff ───
    st.session_state.active_buffs = [
        "✅ 移除【陸軍腐敗】：陸軍組織度 +20%，經驗獲得 +50%",
        "✅ 移除【財政崩潰】：民用工廠建造速度 +30%",
        "✅ 啟動【四億同胞】：核心人力增長 +5.00%",
        "✅ 啟動【漢德軍事合作】：科研速度 +20%，裝甲速度 +15%",
        "✅ 啟動【工業大躍進】：工廠產出 +25%"
    ]

# 3. 頂部資源列 (模擬 HoI4 頂部 HUD)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("📅 遊戲日期", f"{st.session_state.game_date['year']}-{st.session_state.game_date['month']:02d}-{st.session_state.game_date['day']:02d}")
with col2:
    st.metric("👑 政治點數 (PP)", f"{st.session_state.political_power} (+3.5/日)")
with col3:
    st.metric("⚖️ 穩定度", f"{st.session_state.stability}%")
with col4:
    st.metric("🔥 戰爭支持度", f"{st.session_state.war_support}%")
with col5:
    st.metric("👥 可用人力", f"{st.session_state.manpower:,}")
with col6:
    st.metric("🏭 工廠 (民/軍)", f"{st.session_state.civ_factories} / {st.session_state.mil_factories}")

st.markdown("---")

# 4. 側邊欄：國家精神與時間推進
with st.sidebar:
    st.header("⏱️ 時間與战略控制")
    if st.button("▶️ 推進下一天 (Next Day)", use_container_width=True):
        # 時間推進邏輯
        st.session_state.game_date["day"] += 1
        if st.session_state.game_date["day"] > 30:
            st.session_state.game_date["day"] = 1
            st.session_state.game_date["month"] += 1
            if st.session_state.game_date["month"] > 12:
                st.session_state.game_date["month"] = 1
                st.session_state.game_date["year"] += 1
                
        # 每日強大資源產出 (因為有 Buff 加成)
        st.session_state.political_power += 3
        
        # 強大的產能產出：步兵裝備與火砲
        st.session_state.infantry_equipment += int(st.session_state.assigned_mil_inf * 4.5) # Buff 加速生產
        st.session_state.artillery += int(st.session_state.assigned_mil_art * 2.0)
        
        # 國策推進
        if st.session_state.current_focus != "無":
            st.session_state.focus_progress += 1
            if st.session_state.focus_progress >= 35:  # 開啟 Buff：國策時間減半！只需 35 天
                st.session_state.completed_focuses.append(st.session_state.current_focus)
                
                # 國策獎勵
                if st.session_state.current_focus == "🎯 委任令：收回列強租界":
                    st.session_state.political_power += 200
                    st.session_state.stability = min(100, st.session_state.stability + 5)
                    st.session_state.active_buffs.append("✅ 獲得【主權完整】：每日政治點數 +0.5")
                elif st.session_state.current_focus == "🚀 國策：國防重工業五年計劃":
                    st.session_state.mil_factories += 20
                    st.session_state.civ_factories += 10
                    
                st.toast(f"🎉 國策【{st.session_state.current_focus}】提前完成！")
                st.session_state.current_focus = "無"
                st.session_state.focus_progress = 0
        st.rerun()

    st.markdown("---")
    st.header("🔰 當前國家精神 (National Spirits)")
    for buff in st.session_state.active_buffs:
        st.caption(buff)

# 5. 主畫面分頁系統
tab_focus, tab_prod, tab_map = st.tabs(["🎯 專屬國策樹 (Focus)", "🔨 工業產能 (Production)", "🗺️ 全疆域戰略地圖 (Map)"])

# --- TAB 1: 專屬神級國策樹 ---
with tab_focus:
    st.header("🇹🇼 中華民國專屬國策路線（無修正強大版）")
    st.write(f"**當前進行中國策：** {st.session_state.current_focus} ({st.session_state.focus_progress}/35 天) ※已享受國策速度 +100% Buff")
    if st.session_state.current_focus != "無":
        st.progress(st.session_state.focus_progress / 35)
        
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f1_title = "🎯 委任令：收回列強租界"
        disabled_f1 = f1_title in st.session_state.completed_focuses or st.session_state.current_focus != "無"
        if st.button(f"啟動：{f1_title}", disabled=disabled_f1, use_container_width=True):
            st.session_state.current_focus = f1_title
            st.session_state.focus_progress = 0
            st.rerun()
        if f1_title in st.session_state.completed_focuses:
            st.success("✨ 【外交勝利】所有不平等條約已被廢除，租界全部收回！")
            
    with col_f2:
        f2_title = "🚀 國策：國防重工業五年計劃"
        disabled_f2 = f2_title in st.session_state.completed_focuses or st.session_state.current_focus != "無"
        if st.button(f"啟動：{f2_title}", disabled=disabled_f2, use_container_width=True):
            st.session_state.current_focus = f2_title
            st.session_state.focus_progress = 0
            st.rerun()
        if f2_title in st.session_state.completed_focuses:
            st.success("✨ 【工業奇蹟】大後方重工業基地建設完畢，工廠大量增加！")

# --- TAB 2: 工業與軍備產能 ---
with tab_prod:
    st.header("軍事工業生產管理")
    c1, c2 = st.columns(2)
    c1.metric("📦 步兵裝備 I (庫存)", f"{st.session_state.infantry_equipment:,} 件")
    c2.metric("💥 75mm 野戰砲 (庫存)", f"{st.session_state.artillery:,} 門")
    
    st.subheader("分配軍用工廠 (當前可用總數: {})".format(st.session_state.mil_factories))
    
    # 讓玩家滑動調整生產線
    val_inf = st.slider("分配至【步兵裝備】的軍工廠：", 0, st.session_state.mil_factories, st.session_state.assigned_mil_inf)
    val_art = st.slider("分配至【75mm 野戰砲】的軍工廠：", 0, st.session_state.mil_factories - val_inf, st.session_state.assigned_mil_art)
    
    if val_inf != st.session_state.assigned_mil_inf or val_art != st.session_state.assigned_mil_art:
        st.session_state.assigned_mil_inf = val_inf
        st.session_state.assigned_mil_art = val_art
        st.rerun()

# --- TAB 3: 戰略地圖與各省份狀態 ---
with tab_map:
    st.header("中華民國核心領土與守軍狀態")
    map_data = {
        "行省 / 地區": ["南京 (首都圈)", "廣東 (軍閥歸順)", "四川 (大後方)", "平津防線 (前線)"],
        "地形": ["城市/平原", "丘陵", "山地", "要塞都市"],
        "基礎建設": ["10/10 (滿級)", "8/10", "8/10", "10/10 (黃金要塞)"],
        "駐防精銳師團數": ["30 個機械化步兵師", "15 個常備師", "10 個山地師", "40 個德械師 (全裝)"],
        "當地工廠": ["25 國民工廠", "15 工廠", "20 工廠", "20 工廠"]
    }
    st.table(map_data)
