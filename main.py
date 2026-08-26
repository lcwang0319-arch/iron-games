import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 設置網頁
st.set_page_config(page_title="Hearts of Grid IV: 歷史宿怨", page_icon="⚔️", layout="wide")
st.title("⚔️ Hearts of Grid IV: 20×20 列強爭霸（外交仇恨與歷史宿怨版）")

# 2. 定義四個參戰國家的核心色彩
COUNTRIES = ["中華民國", "德意志國", "大日本帝國", "蘇聯"]
COLOR_MAP = {
    "中華民國": "#003399",  # 藍色 🔵
    "德意志國": "#222222",  # 黑色 ⚫
    "大日本帝國": "#ff9999",  # 粉紅色 💗
    "蘇聯": "#cc0000",      # 紅色 🔴
    "中立荒漠": "#444444"    # 灰色 ⚪
}

MAP_SIZE = 20  # 20x20 大地圖

# 3. 系統初始化與選國階段
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_names" not in st.session_state:
    st.session_state.player_names = {c: f"玩家_{i+1}" for i, c in enumerate(COUNTRIES)}

if not st.session_state.game_started:
    st.header("🎮 多人單機模式：請四位玩家分配國家與確認外交仇恨")
    st.markdown("""
    **📢 歐亞外交仇恨值規則：**
    *   **🔥 歷史宿怨**：開局時，**【中華民國】與【大日本帝國】**之間的仇恨值起始即為 **50**。其餘大國互為 **0**。
    *   **⚔️ 宣戰限制**：對特定強權的仇恨值**必須達到 100**，方可下達精準突擊戰令，奪取對方格子！
    *   **📈 仇恨增長**：可以在戰令分頁消耗 PP **主動製造爭端**，或者在盲擴張灰色荒漠時機率爆發邊境衝突！
    """)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_roc = st.text_input("🔵 玩家 1 名字（控制：中華民國）", "玩家_1")
        p_ger = st.text_input("⚫ 玩家 2 名字（控制：德意志國）", "玩家_2")
    with col_p2:
        p_jap = st.text_input("💗 玩家 3 名字（控制：大日本帝國）", "玩家_3")
        p_ussr = st.text_input("🔴 玩家 4 名字（控制：蘇聯）", "玩家_4")
        
    if st.button("🚀 確認天賦與歷史宿怨，大戰正式開打！", type="primary", use_container_width=True):
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

# 初始化 20x20 地圖版圖：帶入蘇聯開局 4 格優勢
# 初始化 20x20 地圖版圖：帶入蘇聯開局 4 格優勢（修正後的正確二維陣列索引）
# 初始化 20x20 地圖版圖：帶入蘇聯開局 4 格優勢（這一次是絕對正確的雙括號寫法！）
# 初始化 20x20 地圖版圖（使用 NumPy 矩陣完全繞過網頁系統吞掉雙括號的 Bug）
if "grid_map" not in st.session_state:
    # 先建立一個 20x20 的中立字串矩陣
    arr = np.full((MAP_SIZE, MAP_SIZE), "中立荒漠", dtype=object)
    
    # 使用逗號分隔座標 arr[列, 行]，這在 Python 裡等同於雙括號，但絕對不會被系統過濾！
    arr[0, 0] = "中華民國"                     # 左上角
    arr[0, MAP_SIZE-1] = "德意志國"             # 右上角
    arr[MAP_SIZE-1, 0] = "大日本帝國"           # 左下角
    
    # 🔴 蘇聯專屬優勢：開局右下角 2x2 共 4 格土地！
    arr[MAP_SIZE-2, MAP_SIZE-2] = "蘇聯"
    arr[MAP_SIZE-2, MAP_SIZE-1] = "蘇聯"
    arr[MAP_SIZE-1, MAP_SIZE-2] = "蘇聯"
    arr[MAP_SIZE-1, MAP_SIZE-1] = "蘇聯"
    
    # 將 NumPy 矩陣轉換回標準 List 儲存到 session_state
    st.session_state.grid_map = arr.tolist()



    grid = [["中立荒漠" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    grid = "中華民國"                # 左上角
    grid[MAP_SIZE-1] = "德意志國"        # 右上角
    grid[MAP_SIZE-1] = "大日本帝國"      # 左下角
    
    # 蘇聯開局 4 格
    grid[MAP_SIZE-2][MAP_SIZE-2] = "蘇聯"
    grid[MAP_SIZE-2][MAP_SIZE-1] = "蘇聯"
    grid[MAP_SIZE-1][MAP_SIZE-2] = "蘇聯"
    grid[MAP_SIZE-1][MAP_SIZE-1] = "蘇聯"
    st.session_state.grid_map = grid

# 初始化四個國家各自獨立的「國家數據」與「外交仇恨值矩陣」
if "player_data" not in st.session_state:
    p_data = {}
    for c in COUNTRIES:
        mp = 6000000
        civ = 8
        if c == "中華民國": mp = 100000000
        if c in ["大日本帝國", "德意志國"]: stock_b, stock_a, t_ok = 30000, 800, "✅ 已解鎖"
        else: stock_b, stock_a, t_ok = 5000, 50, "🔒 未研發"
        if c == "蘇聯": civ = 11
        
        # 初始仇恨值矩陣設定：中日開局 50，其餘皆為 0
        animosity = {enemy: 0 for enemy in COUNTRIES if enemy != c}
        if c == "中華民國": animosity["大日本帝國"] = 50
        if c == "大日本帝國": animosity["中華民國"] = 50
            
        p_data[c] = {
            "pp": 150,
            "manpower": mp,
            "civ_factories": civ,
            "mil_factories": 5,
            "tech": {"中正式步槍": t_ok, "博福斯山砲": t_ok, "中型戰車": "🔒 未研發"},
            "allocation": {"步槍": 3, "火砲": 2, "戰車": 0},
            "stockpile": {"步槍": stock_b, "火砲": stock_a, "戰車": 0},
            "animosity": animosity  # 儲存對其他強權的仇恨值
        }
    st.session_state.player_data = p_data

if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 歷史日誌：中日外交仇恨值已達 50% 臨界點，邊境局勢高度緊張！"]

# 5. 判斷當前玩家與其數據
current_player = COUNTRIES[st.session_state.turn_index]
current_user_name = st.session_state.player_names[current_player]
player_stats = st.session_state.player_data[current_player]

# 6. 頂部資源列 (HUD)
st.subheader(f"👑 目前回合：【{current_user_name}】正在操作 ➔ {current_player} (第 {st.session_state.total_turns} 大回合)")

# 7. 側邊欄：回合結束、情報與當前仇恨值面板
with st.sidebar:
    st.header("⏱️ 回合制戰略中心")
    st.success(f"👉 請【{current_user_name}】完成決策後結束回合。")
    
    if st.button("🏁 結束本回合 (End Turn)", type="primary", use_container_width=True):
        if player_stats["tech"]["中正式步槍"] == "✅ 已解鎖": player_stats["stockpile"]["步槍"] += player_stats["allocation"]["步槍"] * 800
        if player_stats["tech"]["博福斯山砲"] == "✅ 已解鎖": player_stats["stockpile"]["火砲"] += player_stats["allocation"]["火砲"] * 80
        if player_stats["tech"]["中型戰車"] == "✅ 已解鎖": player_stats["stockpile"]["戰車"] += player_stats["allocation"]["戰車"] * 15
        player_stats["pp"] += 60
        
        st.session_state.turn_index += 1
        if st.session_state.turn_index >= 4:
            st.session_state.turn_index = 0
            st.session_state.total_turns += 1
        st.rerun()

    if st.button("🔄 重新整場遊戲（返回選國）", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("📡 我國對各強權仇恨度")
    for enemy, val in player_stats["animosity"].items():
        status = "⚔️ 可宣戰" if val >= 100 else "🕊️ 和平中"
        st.write(f"對【{enemy}】：`{val} / 100` ➔ **{status}**")

    st.markdown("---")
    st.subheader("📜 歐亞前線戰報")
    for log in st.session_state.battle_log[:6]:
        st.caption(log)

# 8. 主畫面分頁
tab_map, tab_tech, tab_action = st.tabs([
    "🗺️ 20×20 史詩多國版圖 (Tactical Board)", 
    "🔬 專屬軍備科研與產線 (Research & Production)", 
    "🎯 戰略專攻與外交戰令 (Military Orders)"
])

# --- TAB 1: 地圖渲染 ---
with tab_map:
    st.header("🗺️ 20×20 巨型割據防區圖 (400格)")
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            owner = st.session_state.grid_map[row][col]
            color = COLOR_MAP[owner]
            rect = plt.Rectangle((col, MAP_SIZE - 1 - row), 1, 1, linewidth=0.5, edgecolor='#222222', facecolor=color, alpha=0.9)
            ax.add_patch(rect)
            if owner != "中立荒漠":
                ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, owner[:2], color='white', ha='center', va='center', fontsize=7, weight='bold')
            elif (row % 4 == 0 and col % 4 == 0):
                ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, f"{row+1},{col+1}", color='#ffffff', ha='center', va='center', fontsize=6, alpha=0.15)
            
    ax.set_xlim(0, MAP_SIZE)
    ax.set_ylim(0, MAP_SIZE)
    ax.set_xticks(range(MAP_SIZE + 1))
    ax.set_yticks(range(MAP_SIZE + 1))
    ax.grid(True, color='#222222', linestyle='-', linewidth=0.5)
    ax.tick_params(colors='white', labelsize=8)
    st.pyplot(fig)
    plt.close(fig)

# --- TAB 2: 科研與產線 ---
with tab_tech:
    st.header(f"🔬 {current_player} 軍工科學院")
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        st.markdown("##### 🔫 中正式步槍 (1936)")
        if player_stats["tech"]["中正式步槍"] == "🔒 未研發" and player_stats["pp"] >= 50:
            if st.button("🧪 消耗 50 PP 研發", key="r_tech"):
                player_stats["pp"] -= 50
                player_stats["tech"]["中正式步槍"] = "✅ 已解鎖"
                st.rerun()
        else: st.write(f"狀態: **{player_stats['tech']['中正式步槍']}**")
    with tc2:
        st.markdown("##### 🍏 博福斯山砲 (1939)")
        if player_stats["tech"]["博福斯山砲"] == "🔒 未研發" and player_stats["pp"] >= 100:
            if st.button("🧪 消耗 100 PP 研發", key="a_tech"):
                player_stats["pp"] -= 100
                player_stats["tech"]["博福斯山砲"] = "✅ 已解鎖"
                st.rerun()
        else: st.write(f"狀態: **{player_stats['tech']['博福斯山砲']}**")
    with tc3:
        st.markdown("##### 🚜 中型戰車 (1941)")
        if player_stats["tech"]["中型戰車"] == "🔒 未研發" and player_stats["pp"] >= 150:
            if st.button("🧪 消耗 150 PP 研發", key="t_tech"):
                player_stats["pp"] -= 150
                player_stats["tech"]["中型戰車"] = "✅ 已解鎖"
                st.rerun()
        else: st.write(f"狀態: **{player_stats['tech']['中型戰車']}**")

    st.markdown("---")
    alloc_rifle = st.number_input("步槍工廠數", 0, player_stats['mil_factories'], player_stats['allocation']['步槍'], key="ar")
    alloc_art = st.number_input("火砲工廠數", 0, player_stats['mil_factories'] - alloc_rifle, player_stats['allocation']['火砲'], key="aa")
    alloc_tank = st.number_input("戰車工廠數", 0, player_stats['mil_factories'] - alloc_rifle - alloc_art, player_stats['allocation']['戰車'], key="at")
    if st.button("⚙️ 儲存本輪產線配置"):
        player_stats['allocation']['步槍'] = alloc_rifle
        player_stats['allocation']['火砲'] = alloc_art
        player_stats['allocation']['戰車'] = alloc_tank
        st.success("產線配置成功更新！")
        st.rerun()

# --- TAB 3: 戰略擴張與外交戰令（核心機制：卡 100 仇恨宣戰） ---
with tab_action:
    st.header(f"🎯 【{current_user_name}】的最高統帥部與外交戰令")
    
    ac1, ac2 = st.columns(2)
    with ac1:
        st.subheader("🛠️ 選項一：精準指定方格突擊（受100仇恨宣戰限制限制）")
        target_row = st.number_input("目標橫列座標 (Row 1-20)", 1, 20, 1)
        target_col = st.number_input("目標縱行座標 (Col 1-20)", 1, 20, 1)
        
        r_idx = target_row - 1
        c_idx = target_col - 1
        current_owner = st.session_state.grid_map[r_idx][c_idx]
        st.write(f"🔍 目標座標 `[{target_row}, {target_col}]` 控制者：**{current_owner}**")
        
        if st.button("⚔️ 下達精準點對點突擊！", type="primary", use_container_width=True):
            if current_owner == current_player:
                st.error("❌ 這是你自己的領土！")
            elif current_owner == "中立荒漠":
                st.session_state.grid_map[r_idx][c_idx] = current_player
                st.session_state.battle_log.insert(0, f"🚩 精準擴張：【{current_user_name}({current_player})】開拓佔領了中立方格 [{target_row}, {target_col}]！")
                player_stats["civ_factories"] += 1
                st.rerun()
            else:
                # 🛑 核心宣戰門檻判定
                current_animosity = player_stats["animosity"][current_owner]
                if current_animosity < 100:
                    st.error(f"🔒 外交限制：你對【{current_owner}】的仇恨值目前僅為 {current_animosity} / 100！在仇恨破百正式宣戰前，雙方部隊無法爆發領土奪取衝突！請先至右側製造外交爭端！")
                else:
                    # 進入真正的對撞流程
                    # 進入真正的對撞流程（仇恨值已達100，解鎖宣戰強攻）
                    enemy_name = st.session_state.player_names[current_owner]
                    enemy_stats = st.session_state.player_data[current_owner]
                    
                    # 計算我軍攻擊力加成
                    r_bonus = 35 if player_stats["stockpile"]["步槍"] > 5000 else -15
                    a_bonus = 50 if player_stats["stockpile"]["火砲"] > 300 else 0
                    t_bonus = 80 if player_stats["stockpile"]["戰車"] > 20 else 0
                    attack_power = 50 + r_bonus + a_bonus + t_bonus + np.random.randint(-15, 15)
                    
                    # 計算敵方防禦力加成
                    enemy_r_bonus = 35 if enemy_stats["stockpile"]["步槍"] > 5000 else -15
                    enemy_a_bonus = 40 if enemy_stats["stockpile"]["火砲"] > 200 else 0
                    defense_power = 60 + enemy_r_bonus + enemy_a_bonus + np.random.randint(-10, 10)
                    
                    # 扣除軍火消耗
                    player_stats["stockpile"]["步槍"] = max(0, player_stats["stockpile"]["步槍"] - 2500)
                    enemy_stats["stockpile"]["步槍"] = max(0, enemy_stats["stockpile"]["步槍"] - 1800)
                    
                    # 🥊 歷史天賦影響：中華民國戰損減半（因為人多），其餘國家正常損耗
                    my_loss = np.random.randint(25000, 75000) if current_player == "中華民國" else np.random.randint(50000, 150000)
                    enemy_loss = np.random.randint(25000, 75000) if current_owner == "中華民國" else np.random.randint(50000, 150000)
                    
                    player_stats["manpower"] = max(0, player_stats["manpower"] - my_loss)
                    enemy_stats["manpower"] = max(0, enemy_stats["manpower"] - enemy_loss)
                    
                    # 判定勝負
                    if attack_power > defense_power:
                        st.session_state.grid_map[r_idx][c_idx] = current_player
                        st.session_state.battle_log.insert(0, f"💥 捷報！【{current_user_name}({current_player})】突破 100 仇恨全面宣戰！成功強奪了【{enemy_name}({current_owner})】的領地 [{target_row}, {target_col}]！")
                    else:
                        st.session_state.battle_log.insert(0, f"🛡️ 戰敗：【{current_user_name}({current_player})】向【{enemy_name}】的 [{target_row}, {target_col}] 領地發起猛烈強攻，但被對方的防線死守擊退！")
                    st.rerun()

    with ac2:
        st.subheader("⚡ 選項二：集團軍拓荒與「外交製造爭端」")
        
        # 1. 製造爭端按鈕
        st.markdown("##### 📡 統帥部外交部：主動挑釁（提升仇恨值）")
        provoke_target = st.selectbox("請選擇你要主動挑釁、製造地緣政治摩擦的國家：", [c for c in COUNTRIES if c != current_player])
        
        if st.button(f"🔥 消耗 30 PP 製造爭端，挑釁【{provoke_target}】", use_container_width=True):
            if player_stats["pp"] >= 30:
                player_stats["pp"] -= 30
                # 雙向仇恨同步增加 15-25 點
                gain = np.random.randint(15, 26)
                player_stats["animosity"][provoke_target] = min(100, player_stats["animosity"][provoke_target] + gain)
                st.session_state.player_data[provoke_target]["animosity"][current_player] = min(100, st.session_state.player_data[provoke_target]["animosity"][current_player] + gain)
                st.session_state.battle_log.insert(0, f"📡 外交挑釁：【{current_user_name}({current_player})】在邊境故意尋釁滋事，與【{provoke_target}】的雙向仇恨值暴增 {gain} 點！")
                st.rerun()
            else:
                st.error("❌ 政治點數不足 30 PP，外交官無法發動主動挑釁！")
                
        st.markdown("---")
        # 2. 集團軍拓荒按鈕
        st.markdown("##### 🚀 啟動集團軍：閃擊大範圍拓荒 (消耗 40 PP)")
        st.caption("隨機吞併 1~5 格中立灰色荒漠。在中原瘋狂擴張的同時，有 35% 機率隨機引爆邊境摩擦，導致隨機大國對你的仇恨度飆升！")
        
        if st.button("發動集團軍拓荒！", use_container_width=True):
            if player_stats["pp"] >= 40:
                player_stats["pp"] -= 40
                neutral_coords = []
                for r in range(MAP_SIZE):
                    for c in range(MAP_SIZE):
                        if st.session_state.grid_map[r][c] == "中立荒漠":
                            neutral_coords.append((r, c))
                
                if neutral_coords:
                    conquest_count = min(len(neutral_coords), np.random.randint(1, 6))
                    chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]
                    for r, c in chosen_spots:
                        st.session_state.grid_map[r][c] = current_player
                    
                    player_stats["civ_factories"] += conquest_count
                    player_stats["stockpile"]["步槍"] += conquest_count * 500
                    st.session_state.battle_log.insert(0, f"⚡ 拓荒：【{current_user_name}({current_player})】擴張吞併了 {conquest_count} 格中立區，工廠產線規模擴大！")
                    
                    # ⚠️ 機率觸發邊境仇恨摩擦
                    if np.random.rand() < 0.35:
                        other_countries = [c for c in COUNTRIES if c != current_player]
                        hit_country = np.random.choice(other_countries)
                        clash_gain = np.random.randint(10, 21)
                        player_stats["animosity"][hit_country] = min(100, player_stats["animosity"][hit_country] + clash_gain)
                        st.session_state.player_data[hit_country]["animosity"][current_player] = min(100, st.session_state.player_data[hit_country]["animosity"][current_player] + clash_gain)
                        st.session_state.battle_log.insert(0, f"💥 邊境擦槍走火！我軍在開拓邊疆時與【{hit_country}】守軍發生零星摩擦，雙方仇恨飆升 {clash_gain} 點！")
                    st.rerun()
                else:
                    st.error("❌ 全地圖中立荒漠已被瓜分完畢！")
            else:
                st.error("❌ 政治點數不足 40 PP！")
