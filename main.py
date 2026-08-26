import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Grid IV: 20x20巨型爭霸", page_icon="⚔️", layout="wide")
st.title("⚔️ Hearts of Grid IV: 巨型歐亞方格爭霸（20×20 史詩大戰場）")

# 2. 定義四個參戰國家的核心色彩與基礎數值
COUNTRIES = ["中華民國", "德意志國", "大日本帝國", "蘇聯"]
COLOR_MAP = {
    "中華民國": "#003399",  # 藍色 🔵
    "德意志國": "#222222",  # 黑色 ⚫
    "大日本帝國": "#ff9999",  # 粉紅色 💗
    "蘇聯": "#cc0000",      # 紅色 🔴
    "中立荒漠": "#444444"    # 灰色 ⚪
}

MAP_SIZE = 20  # 升級為 20x20 大地圖

# 3. 系統初始化與選國階段
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_names" not in st.session_state:
    st.session_state.player_names = {c: f"玩家_{i+1}" for i, c in enumerate(COUNTRIES)}

if not st.session_state.game_started:
    st.header("🎮 歡迎進入 20×20 多人單機模式：請四位玩家分配國家")
    st.markdown("戰場已擴張至 **400 格巨型矩陣**！請輸入每位玩家的名字，每人控制一個國家，從角落出發吞併天下！")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_roc = st.text_input("🔵 玩家 1 名字（控制：中華民國）", "玩家_1")
        p_ger = st.text_input("⚫ 玩家 2 名字（控制：德意志國）", "玩家_2")
    with col_p2:
        p_jap = st.text_input("💗 玩家 3 名字（控制：大日本帝國）", "玩家_3")
        p_ussr = st.text_input("🔴 玩家 4 名字（控制：蘇聯）", "玩家_4")
        
    if st.button("🚀 分配完畢，史詩大戰正式開打！", type="primary", use_container_width=True):
        st.session_state.player_names["中華民國"] = p_roc
        st.session_state.player_names["德意志國"] = p_ger
        st.session_state.player_names["大日本帝國"] = p_jap
        st.session_state.player_names["蘇聯"] = p_ussr
        st.session_state.game_started = True
        st.rerun()
    st.stop()

# 4. 遊戲核心數據防禦性初始化
if "turn_index" not in st.session_state:
    st.session_state.turn_index = 0  
if "total_turns" not in st.session_state:
    st.session_state.total_turns = 1

# 初始化 20x20 地圖版圖：大家開局都只有角落的 1 格
if "grid_map" not in st.session_state:
    grid = [["中立荒漠" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    grid[0][0] = "中華民國"                # 左上角 [1, 1]
    grid[0][MAP_SIZE-1] = "德意志國"        # 右上角 [1, 20]
    grid[MAP_SIZE-1][0] = "大日本帝國"      # 左下角 [20, 1]
    grid[MAP_SIZE-1][MAP_SIZE-1] = "蘇聯"  # 右下角 [20, 20]
    st.session_state.grid_map = grid

# 初始化四個國家各自獨立的「國家數據」
if "player_data" not in st.session_state:
    p_data = {}
    for c in COUNTRIES:
        p_data[c] = {
            "pp": 150,
            "manpower": 8000000,
            "civ_factories": 8,
            "mil_factories": 5,
            "tech": {"中正式步槍": "🔒 未研發", "博福斯山砲": "🔒 未研發", "中型戰車": "🔒 未研發"},
            "allocation": {"步槍": 3, "火砲": 2, "戰車": 0},
            "stockpile": {"步槍": 15000, "火砲": 300, "戰車": 0}
        }
    st.session_state.player_data = p_data

if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 遊戲開始！20×20 歐亞大棋盤啟動，400格領地爭奪戰打響。"]

# 5. 判斷當前輪到哪位玩家與對應名字
current_player = COUNTRIES[st.session_state.turn_index]
current_user_name = st.session_state.player_names[current_player]
player_stats = st.session_state.player_data[current_player]

# 6. 頂部資源列 (HUD) - 即時動態切換顯示當前玩家的數據
st.subheader(f"👑 目前回合：【{current_user_name}】正在操作 ➔ {current_player} (第 {st.session_state.total_turns} 大回合)")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("👑 政治點數 (PP)", f"{player_stats['pp']}")
with col2:
    st.metric("👥 可用人力", f"{player_stats['manpower']:,}")
with col3:
    st.metric("🏭 工廠 (民/軍)", f"{player_stats['civ_factories']} / {player_stats['mil_factories']}")
with col4:
    st.metric("🔫 步槍 / 🍏 火砲庫存", f"{player_stats['stockpile']['步槍']:,} / {player_stats['stockpile']['火砲']:,}")
with col5:
    st.metric("🚜 戰車庫存", f"{player_stats['stockpile']['戰車']:,} 輛")

st.markdown("---")

# 7. 側邊欄：回合結束與戰報
with st.sidebar:
    st.header("⏱️ 回合制戰略中心")
    st.success(f"👉 請 🌟【{current_user_name}】🌟 進行本輪決策，確認完「科研、產線與下達指令」後，點擊結束回合。")
    
    if st.button("🏁 結束本回合 (End Turn)", type="primary", use_container_width=True):
        # 結算當前玩家武器產出
        if player_stats["tech"]["中正式步槍"] == "✅ 已解鎖":
            player_stats["stockpile"]["步槍"] += player_stats["allocation"]["步槍"] * 800
        if player_stats["tech"]["博福斯山砲"] == "✅ 已解鎖":
            player_stats["stockpile"]["火砲"] += player_stats["allocation"]["火砲"] * 80
        if player_stats["tech"]["中型戰車"] == "✅ 已解鎖":
            player_stats["stockpile"]["戰車"] += player_stats["allocation"]["戰車"] * 15
            
        # 20x20 大地圖每回合被動發放更多 PP (大圖發展更流暢)
        player_stats["pp"] += 60
        
        # 輪流切換到下一個玩家
        st.session_state.turn_index += 1
        if st.session_state.turn_index >= 4:
            st.session_state.turn_index = 0
            st.session_state.total_turns += 1
            
        st.rerun()

    if st.button("🔄 重新整場遊戲（返回選國）", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("📜 歐亞戰線實時日誌")
    for log in st.session_state.battle_log[:10]:
        st.caption(log)

# 8. 主畫面分頁
tab_map, tab_tech, tab_action = st.tabs([
    "🗺️ 20×20 史詩多國版圖 (Tactical Board)", 
    "🔬 專屬軍備科研與產線 (Research & Production)", 
    "🎯 戰略專攻與大擴張戰令 (Military Orders)"
])

# --- TAB 1: 20×20 多國色塊版圖（完美體現你手繪的方格風格與指定色彩） ---
with tab_map:
    st.header("🗺️ 20×20 巨型微觀防區爭奪圖 (共400格)")
    st.caption(f"🔵 中華民國 ({st.session_state.player_names['中華民國']}) | ⚫ 德意志國 ({st.session_state.player_names['德意志國']}) | 💗 大日本帝國 ({st.session_state.player_names['大日本帝國']}) | 🔴 蘇聯 ({st.session_state.player_names['蘇聯']}) | ⚪ 中立荒漠")
    
    # 20x20 圖形較大，拉高畫布尺寸避免擠壓
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    
    # 渲染 20x20 方格
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            owner = st.session_state.grid_map[row][col]
            color = COLOR_MAP[owner]
            
            # 繪製格子，格子縮小間距更細緻
            rect = plt.Rectangle((col, MAP_SIZE - 1 - row), 1, 1, linewidth=0.5, edgecolor='#222222', facecolor=color, alpha=0.9)
            ax.add_patch(rect)
            
            # 因為格子有 400 格，只有當非中立或者是極端角落時才顯示簡稱，避免畫面文字爆炸
            if owner != "中立荒漠":
                ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, owner[:2], 
                         color='white', ha='center', va='center', fontsize=7, weight='bold')
            elif (row % 4 == 0 and col % 4 == 0): # 中立荒漠每隔 4 格淡淡標註一次座標
                ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, f"{row+1},{col+1}", 
                         color='#ffffff', ha='center', va='center', fontsize=6, alpha=0.2)
            
    ax.set_xlim(0, MAP_SIZE)
    ax.set_ylim(0, MAP_SIZE)
    ax.set_xticks(range(MAP_SIZE + 1))
    ax.set_yticks(range(MAP_SIZE + 1))
    ax.grid(True, color='#222222', linestyle='-', linewidth=0.5)
    ax.tick_params(colors='white', labelsize=8)
    st.pyplot(fig)
    plt.close(fig)
    
    # 計算各國目前的總領土格子數
    st.subheader("📊 戰界領土割據統計 (400格)")
    counts = {"中華民國": 0, "德意志國": 0, "大日本帝國": 0, "蘇聯": 0, "中立荒漠": 0}
    for r in range(MAP_SIZE):
        for c in range(MAP_SIZE):
            counts[st.session_state.grid_map[r][c]] += 1
            
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric(f"🔵 中華民國 ({st.session_state.player_names['中華民國']})", f"{counts['中華民國']} / 400 格")
    mc2.metric(f"⚫ 德意志國 ({st.session_state.player_names['德意志國']})", f"{counts['德意志國']} / 400 格")
    mc3.metric(f"💗 大日本帝國 ({st.session_state.player_names['大日本帝國']})", f"{counts['大日本帝國']} / 400 格")
    mc4.metric(f"🔴 蘇聯 ({st.session_state.player_names['蘇聯']})", f"{counts['蘇聯']} / 400 格")

# --- TAB 2: 科研與產線管理 ---
with tab_tech:
    st.header(f"🔬 【{current_user_name}】的 {current_player} 軍工科學院")
    
    st.subheader("💡 獨立軍備科研（解鎖量產資格）")
    tc1, tc2, tc3 = st.columns(3)
    
    with tc1:
        st.markdown("##### 🔫 輕武器研發")
        rifle_status = player_stats["tech"]["中正式步槍"]
        st.write(f"狀態: **{rifle_status}**")
        if rifle_status == "🔒 未研發" and player_stats["pp"] >= 50:
            if st.button("🧪 消耗 50 PP 研發【中正式步槍】"):
                player_stats["pp"] -= 50
                player_stats["tech"]["中正式步槍"] = "✅ 已解鎖"
                st.success("研發成功！解鎖步槍量產產線。")
                st.rerun()
                
    with tc2:
        st.markdown("##### 🍏 重火砲研發")
        art_status = player_stats["tech"]["博福斯山砲"]
        st.write(f"狀態: **{art_status}**")
        if art_status == "🔒 未研發" and player_stats["pp"] >= 100:
            if st.button("🧪 消耗 100 PP 研發【博福斯山砲】"):
                player_stats["pp"] -= 100
                player_stats["tech"]["博福斯山砲"] = "✅ 已解鎖"
                st.success("研發成功！解鎖火砲量產產線。")
                st.rerun()
                
    with tc3:
        st.markdown("##### 🚜 裝甲戰車研發")
        tank_status = player_stats["tech"]["中型戰車"]
        st.write(f"狀態: **{tank_status}**")
        if tank_status == "🔒 未研發" and player_stats["pp"] >= 150:
            if st.button("🧪 消耗 150 PP 研發【中型戰車】"):
                player_stats["pp"] -= 150
                player_stats["tech"]["中型戰車"] = "✅ 已解鎖"
                st.success("研發成功！解鎖戰車裝甲產線。")
                st.rerun()

    st.markdown("---")
    st.subheader("🏭 本輪軍用工廠產線分配")
    st.caption(f"你目前擁有 {player_stats['mil_factories']} 座軍工廠。請調配本回合產出的武器類別：")
    
    alloc_rifle = st.number_input("步槍工廠數", 0, player_stats['mil_factories'], player_stats['allocation']['步槍'], key="ar")
    alloc_art = st.number_input("火砲工廠數", 0, player_stats['mil_factories'] - alloc_rifle, player_stats['allocation']['火砲'], key="aa")
    alloc_tank = st.number_input("戰車工廠數", 0, player_stats['mil_factories'] - alloc_rifle - alloc_art, player_stats['allocation']['戰車'], key="at")
    
    if st.button("⚙️ 儲存本輪產線配置"):
        player_stats['allocation']['步槍'] = alloc_rifle
        player_stats['allocation']['火砲'] = alloc_art
        player_stats['allocation']['戰車'] = alloc_tank
        st.success("產線配置更新！")
        st.rerun()

# --- TAB 3: 戰略專攻與大擴張（新增集團軍閃擊拓荒） ---
with tab_action:
    st.header(f"🎯 【{current_user_name}】的最高統帥戰令")
    st.caption("20×20 大地圖模式下，你可以自由選擇精準突擊特定格子，或者使用集團軍大面積往特定方向擴張中立區！")
    
    ac1, ac2 = st.columns(2)
    with ac1:
        st.subheader("🛠️ 選項一：精準指定方格突擊（適合與敵軍正面交火）")
        target_row = st.number_input("目標橫列座標 (Row 1-20)", 1, 20, 1)
        target_col = st.number_input("目標縱行座標 (Col 1-20)", 1, 20, 1)
        
        # 轉換為 0-indexed 陣列索引
        r_idx = target_row - 1
        c_idx = target_col - 1
        current_owner = st.session_state.grid_map[r_idx][c_idx]
        st.write(f"🔍 目標座標 `[{target_row}, {target_col}]` 控制者：**{current_owner}**" + (f" ({st.session_state.player_names[current_owner]})" if current_owner != "中立荒漠" else ""))
        
        if st.button("⚔️ 下達精準點對點突擊！", type="primary", use_container_width=True):
            if current_owner == current_player:
                st.error("❌ 這是你自己的領土！請選擇其他格子擴張或進攻！")
            elif current_owner == "中立荒漠":
                st.session_state.grid_map[r_idx][c_idx] = current_player
                st.session_state.battle_log.insert(0, f"🚩 精準擴張：【{current_user_name}({current_player})】佔領了中立方格 [{target_row}, {target_col}]！")
                player_stats["civ_factories"] += 1
                st.rerun()
            else:
                # 敵對玩家格子對撞機制
                enemy_name = st.session_state.player_names[current_owner]
                r_bonus = 30 if player_stats["stockpile"]["步槍"] > 5000 else 0
                a_bonus = 45 if player_stats["stockpile"]["火砲"] > 300 else 0
                t_bonus = 70 if player_stats["stockpile"]["戰車"] > 20 else 0
                attack_power = 50 + r_bonus + a_bonus + t_bonus + np.random.randint(-15, 15)
                
                enemy_stats = st.session_state.player_data[current_owner]
                enemy_r_bonus = 30 if enemy_stats["stockpile"]["步槍"] > 5000 else 0
                defense_power = 60 + enemy_r_bonus + np.random.randint(-10, 10)
                
                # 扣除雙方軍火與人力損耗
                player_stats["stockpile"]["步槍"] = max(0, player_stats["stockpile"]["步槍"] - 2500)
                enemy_stats["stockpile"]["步槍"] = max(0, enemy_stats["stockpile"]["步槍"] - 1800)
                player_stats["manpower"] = max(0, player_stats["manpower"] - np.random.randint(60000, 150000))
                enemy_stats["manpower"] = max(0, enemy_stats["manpower"] - np.random.randint(40000, 120000))
                
                # 判定勝負與改染地圖色塊
                if attack_power > defense_power:
                    st.session_state.grid_map[r_idx][c_idx] = current_player
                    st.session_state.battle_log.insert(0, f"💥 捷報！【{current_user_name}({current_player})】突擊成功，強奪了【{enemy_name}({current_owner})】的要塞格子 [{target_row}, {target_col}]！")
                else:
                    st.session_state.battle_log.insert(0, f"🛡️ 戰敗：【{current_user_name}({current_player})】對 [{target_row}, {target_col}] 的精準強攻被【{enemy_name}】死守擊退！")
                st.rerun()

    with ac2:
        st.subheader("⚡ 選項二：集團軍大範圍盲擴張（專為 20×20 大圖設計！）")
        st.markdown("由於地圖高達 **400 格**，你可以花費 **40 點政治點數 (PP)** 啟動集團軍突擊，系統會自動在全圖尋找中立灰色荒漠，並**瞬間連續橫掃強佔 1 ~ 5 個格子**，極速擴張後方基地與產線！")
        
        if st.button("🚀 啟動集團軍：閃擊大範圍拓荒！", use_container_width=True):
            if player_stats["pp"] >= 40:
                player_stats["pp"] -= 40
                
                # 在 20x20 地圖中尋找所有中立格子
                neutral_coords = []
                for r in range(MAP_SIZE):
                    for c in range(MAP_SIZE):
                        if st.session_state.grid_map[r][c] == "中立荒漠":
                            neutral_coords.append((r, c))
                
                if neutral_coords:
                    # 隨機吞併 1~5 格中立土地
                    conquest_count = min(len(neutral_coords), np.random.randint(1, 6))
                    chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]
                    
                    for r, c in chosen_spots:
                        st.session_state.grid_map[r][c] = current_player
                    
                    # 獎勵民用工廠（每一格搶到的中立土地都提供1座民工廠產能）
                    player_stats["civ_factories"] += conquest_count
                    # 拓荒隨機挖到前朝軍火庫，加碼補給步槍庫存
                    player_stats["stockpile"]["步槍"] += conquest_count * 500
                    
                    st.session_state.battle_log.insert(0, f"⚡ 閃擊戰：【{current_user_name}({current_player})】集團軍發動大開拓，一口氣橫掃吞併了 {conquest_count} 格中立荒漠，民工廠 +{conquest_count}！")
                    st.rerun()
                else:
                    st.error("❌ 全地圖中立荒漠已被瓜分完畢，無法再使用大範圍盲擴張！請改用選項一精準突擊對手領土！")
            else:
                st.error("❌ 政治點數不足 40 PP，無法發動集團軍大規模盲擴裝！")
                
        st.markdown("---")
        st.info("""
        **💡 20×20 史詩回合制大戰策略：**
        1. **前期（第 1 ~ 15 回合）**：全場 400 格大片都是灰色。請每位玩家在自己的回合瘋狂點選右邊的 **【選項二：集團軍閃擊盲擴張】**。一次可以搶到 1~5 格，迅速把民用工廠和基礎步槍庫存堆起來！
        2. **中期（科研與整軍）**：利用搶地盤帶來的巨額民用工廠優勢，在【軍工科學院】瘋狂點步槍、大砲和坦克科研，將產線拉滿，儲備戰爭物資。
        3. **後期（方格吞併大決戰）**：當四個人的色塊在 20×20 大棋盤中間全面撞車時，轉用 **【選項一：精準指定座標突擊】**，直接輸入對方的座標格子，用你的坦克大砲強行把敵人的領土染成你的顏色！
        """)
