import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Streamlit IV: 中華民國崛起", page_icon="🇹🇼", layout="wide")
st.title("🇹🇼 Hearts of Streamlit IV: 中華民國（完全體天警開局 · 手繪風戰線版）")

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

# --- 提取手繪風格新增的戰術矩陣變數 ---
if "combat_grid" not in st.session_state:
    # 0 代表敵方/未爭奪（紅），1 代表我方攻克（藍）。初始有幾個隨機前線格子
    st.session_state.combat_grid = np.zeros((5, 5), dtype=int)
if "completed_focuses" not in st.session_state:
    st.session_state.completed_focuses = []
if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 1936年1月1日：軍事委員會已下達最高動員令，前線部隊進入臨戰狀態。"]

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
    st.metric("🏭 工廠 (民/軍)", f"{st.session_state.civ_factories} / {st.session_state.mil_factories}")
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
        
        # 每日增長 PP
        st.session_state.political_power += 2
        
        # 緊張度隨歷史推進增長
        if st.session_state.world_tension < 100:
            st.session_state.world_tension = min(100, st.session_state.world_tension + 1)
            
        # ⚔️ 模擬手繪風格的「前線微觀方格爭奪」
        if st.session_state.war_declared and np.sum(st.session_state.combat_grid) < 25:
            # 計算成功率：有軍事國策加成會大幅提高
            success_rate = 0.5 if "漢陽兵工廠產能全開" in st.session_state.completed_focuses else 0.25
            
            if np.random.rand() < success_rate:
                # 隨機找一個還是 0 (敵方) 的格子染成 1 (我方)
                zero_indices = np.argwhere(st.session_state.combat_grid == 0)
                if len(zero_indices) > 0:
                    chosen_idx = zero_indices[np.random.choice(len(zero_indices))]
                    st.session_state.combat_grid[chosen_idx[0], chosen_idx[1]] = 1
                    st.session_state.battle_log.insert(0, f"💥 捷報！我軍成功突破前線方格座標 [{chosen_idx[0]+1}, {chosen_idx[1]+1}]！")
            else:
                st.session_state.battle_log.insert(0, f"⏳ 前線拉鋸中：我軍德械師正與敵方在方格防線激烈交火...")
            
            # 戰時人力損耗
            st.session_state.manpower = max(0, st.session_state.manpower - int(np.random.randint(10000, 35000)))
            
        st.rerun()

    if st.button("🔄 重設全域數據", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.header("🔰 當前國家精神")
    for buff in st.session_state.active_buffs:
        st.caption(buff)

# 5. 主畫面分頁 (新增國策樹分頁)
tab_map, tab_focus, tab_diplomacy = st.tabs([
    "🗺️ 秋海棠疆域最高統帥部 (Military Map)", 
    "🌳 國家復興國策樹 (Focus Tree)", 
    "🌍 國際外交與前線戰報 (Diplomacy)"
])

# --- TAB 1: 戰略地圖（保留宏觀歷史地圖，下方加入微觀手繪風方格戰線） ---
with tab_map:
    st.header("🎯 最高統帥部戰略地圖")
    
    # 宏觀秋海棠歷史地圖（原本的 Matplotlib 渲染）
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    t = np.linspace(0, 2*np.pi, 100)
    x = 12 * np.cos(t) + 3 * np.sin(2*t) + 100
    y = 8 * np.sin(t) + 2 * np.cos(3*t) + 35
    ax.fill(x, y, color='#003399', alpha=0.6, label='ROC Core Territory (秋海棠疆域)')
    
    defense_x = [118, 116, 113, 123]
    defense_y = [32, 39, 23, 41]
    defense_names = ['Nanjing', 'Pingjin', 'Guangdong', 'Guanwai']
    ax.scatter(defense_x, defense_y, color='#ff0000', s=120, zorder=5, label='精銳德械師駐防要塞')
    for i, txt in enumerate(defense_names):
        ax.annotate(txt, (defense_x[i]+0.5, defense_y[i]+0.5), color='white', fontsize=11, weight='bold')

    if st.session_state.war_declared:
        ax.arrow(116, 39, 5, 5, head_width=1.5, head_length=2, fc='#ff3333', ec='#ff3333', label='戰線全線反攻推進中')
        ax.arrow(123, 41, 4, -2, head_width=1.5, head_length=2, fc='#ff3333', ec='#ff3333')
    
    ax.set_title("Republic of China - Theater Strategy Map", color='white', fontsize=14, weight='bold')
    ax.grid(True, color='#333333', linestyle='--')
    ax.tick_params(colors='white')
    ax.legend(loc='lower left', facecolor='#222222', edgecolor='white', labelcolor='white')
    st.pyplot(fig)
    plt.close(fig) # 防記憶體洩漏

    st.markdown("---")
    
    # 🪓 全新加入：引進手繪風格的「前線微觀戰術方格窗」
    st.subheader("🎨 前線戰術方格動態窗 (Micro Combat Grid)")
    st.caption("以下矩陣代表戰區前線的微觀推進。藍色方格代表我軍已攻克的防區，紅色虛線方格代表敵軍死守的陣地（靈感源自手繪軍事防區設定）。")
    
    fig_grid, ax_grid = plt.subplots(figsize=(6, 5), facecolor='#1e1e1e')
    ax_grid.set_facecolor('#111111')
    
    # 畫出 5x5 的矩陣格子
    for row in range(5):
        for col in range(5):
            is_captured = st.session_state.combat_grid[row, col] == 1
            color = '#00aaff' if is_captured else '#ff3333'
            style = '-' if is_captured else '--'
            alpha = 0.7 if is_captured else 0.2
            
            rect = plt.Rectangle((col, 4-row), 1, 1, linewidth=2, edgecolor=color, facecolor=color, alpha=alpha, linestyle=style)
            ax_grid.add_patch(rect)
            
            # 格子內座標文字
            ax_grid.text(col+0.5, 4-row+0.5, f"{row+1},{col+1}", color='white', ha='center', va='center', fontsize=9, alpha=0.6)
            
    ax_grid.set_xlim(0, 5)
    ax_grid.set_ylim(0, 5)
    ax_grid.axis('off')
    ax_grid.set_title("Tactical Sector Breakdown - Frontline Control", color='white', fontsize=12, weight='bold')
    
    col_map1, col_map2 = st.columns([2, 1])
    with col_map1:
        st.pyplot(fig_grid)
        plt.close(fig_grid)
    with col_map2:
        captured_grid_count = np.sum(st.session_state.combat_grid)
        st.metric("🎯 已收復前線方格", f"{captured_grid_count} / 25")
        grid_pct = (captured_grid_count / 25.0)
        st.progress(grid_pct, text=f"戰區總淨化度: {int(grid_pct*100)}%")

# --- TAB 2: 中華民國專屬國策樹（全新功能連動！） ---
with tab_focus:
    st.header("🌳 國家復興精神：中央國策樹系統")
    st.caption("消耗政治點數（PP）來點選國策，解鎖強大 Buff 並顯著提升前線方格的奪取機率。")
    
    col_tree1, col_tree2 = st.columns(2)
    
    with col_tree1:
        st.subheader("⚔️ 軍事工業線")
        if "漢陽兵工廠產能全開" not in st.session_state.completed_focuses:
            if st.button("📌 推進國策：【漢陽兵工廠產能全開】(花費 150 PP)", use_container_width=True):
                if st.session_state.political_power >= 150:
                    st.session_state.political_power -= 150
                    st.session_state.completed_focuses.append("漢陽兵工廠產能全開")
                    st.session_state.mil_factories += 25
                    st.session_state.active_buffs.append("🔥 漢陽火砲：前線微觀方格突破成功率大幅翻倍！")
                    st.success("國策完成！軍工廠 +25，前線推格子的判定機率大增！")
                    st.rerun()
                else: st.error("❌ 政治點數不足！")
        else:
            st.button("✅ 【漢陽兵工廠產能全開】(已完成)", disabled=True, use_container_width=True)

    with col_tree2:
        st.subheader("🏗️ 後方經濟線")
        if "國防重工業現代化" not in st.session_state.completed_focuses:
            if st.button("📌 推進國策：【重工業基地建設】(花費 120 PP)", use_container_width=True):
                if st.session_state.political_power >= 120:
                    st.session_state.political_power -= 120
                    st.session_state.completed_focuses.append("國防重工業現代化")
                    st.session_state.civ_factories += 35
                    st.session_state.stability = min(100, st.session_state.stability + 10)
                    st.session_state.active_buffs.append("⚡ 工業奇蹟：每日政治點數產出效率提升")
                    st.success("國策完成！民用工廠 +35，後方經濟基礎穩固！")
                    st.rerun()
                else: st.error("❌ 政治點數不足！")
        else:
            st.button("✅ 【重工業基地建設】(已完成)", disabled=True, use_container_width=True)

# --- TAB 3: 國際外交與雷達局勢圖 ---
with tab_diplomacy:
    st.header("🌍 遠東與全球國際外交戰線")
    
    # 國際關係雷達圖（融入國策完成度）
    labels = np.array(['Stability', 'War Support', 'Industry', 'Manpower', 'Focus Trait'])
    focus_score = len(st.session_state.completed_focuses) * 50 + 10
    stats = np.array([st.session_state.stability, st.session_state.war_support, 85, 95, min(100, focus_score)])
    
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    # 2. 雷達圖角度與數據首尾閉合處理（修復受手繪啟發的雷達數據閉合）
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    
    # 將數據陣列與角度陣列都複製首個元素到尾端，確保雷達圖 360 度完全閉合
    stats_closed = np.concatenate((stats, [stats[0]]))
    angles_closed = angles + [angles[0]]
    
    # 3. 開始繪製雷達圖
    fig_radar, ax_radar = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), facecolor='#1e1e1e')
    ax_radar.set_facecolor('#111111')
    
    # 填滿與繪製雷達圖折線
    ax_radar.fill(angles_closed, stats_closed, color='#ffcc00', alpha=0.4, label='中華民國實力雷達')
    ax_radar.plot(angles_closed, stats_closed, color='#ffcc00', linewidth=2)
    
    # 設置雷達圖五角座標標籤與網格線
    ax_radar.set_thetagrids(np.degrees(angles), labels, color='white', fontsize=12, weight='bold')
    ax_radar.set_rgrids([20, 40, 60, 80, 100], labels=[], color='#444444')
    ax_radar.tick_params(colors='white')
    ax_radar.set_title("Global Geopolitical Influence Radar", color='white', fontsize=14, weight='bold', pad=20)
    
    # 渲染雷達圖並關閉畫布（防止記憶體洩漏）
    st.pyplot(fig_radar)
    plt.close(fig_radar) 
    
    st.markdown("---")
    st.subheader("📡 前線戰略抉擇與即時戰報")
    
    if not st.session_state.war_declared:
        st.info("💡 歷史評估：我方已全面移除所有歷史枷鎖，隨時可以拒絕承認列強不平等條約。")
        if st.button("💥 拒絕對列強妥協：向軸心國與不平等條約宣戰！", type="primary", use_container_width=True):
            st.session_state.war_declared = True
            st.session_state.world_tension = min(100, st.session_state.world_tension + 45)
            st.rerun()
    else:
        total_captured = np.sum(st.session_state.combat_grid)
        if total_captured < 25:
            st.error("⚔️ 【全面戰爭狀態】我方已對全球帝國主義宣戰！")
            st.warning("⏳ 戰略指令：請回到【最高統帥部】查看手繪風方格戰區。點擊側邊欄的「▶️ 推進下一天」可以模擬每日強攻並蠶食敵方格子的過程！")
        else:
            st.balloons()
            st.success("🏆 【全戰區大勝利】前線 25 個戰術方格已被我軍精銳德械師全部收復、悉數染藍！")
            
        # 顯示即時戰報日誌
        st.markdown("### 📜 戰區前線實時電報")
        for log in st.session_state.battle_log[:6]: # 僅顯示最新 6 條
            st.write(log)
