import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 設置網頁（完全無痕偽裝，抹除所有整蠱與解體字眼）
st.set_page_config(page_title="Hearts of Grid IV: 歐亞群雄戰紀", page_icon="⚔️", layout="wide")
st.title("⚔️ Hearts of Grid IV: 歐亞群雄戰紀（多人單機 · 熱座回合制完全體）")

# 2. 定義四個參戰國家與割據勢力的核心色彩
COUNTRIES = ["中華民國", "德意志國", "大日本帝國", "蘇聯"]
COLOR_MAP = {
    "中華民國": "#003399",  # 藍色 🔵
    "德意志國": "#222222",  # 黑色 ⚫
    "大日本帝國": "#ff9999",  # 粉紅色 💗
    "蘇聯": "#cc0000",      # 紅色 🔴
    "地方軍閥": "#e67e22",  # 深橘色 🥮 (包圍中華民國)
    "法西斯蘇聯": "#ffffff",  # 白色 ⚪ (內部隱藏機制)
    "民主蘇聯": "#ffcc00",    # 黃色 🟡 (內部隱藏機制)
    "君主蘇聯": "#22aa22",    # 綠色 🟢 (內部隱藏機制)
    "中立荒漠": "#444444"    # 灰色 🟤
}

MAP_SIZE = 20  # 20x20 大地圖

# 3. 系統初始化與選國階段
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_names" not in st.session_state:
    st.session_state.player_names = {c: f"玩家_{i+1}" for i, c in enumerate(COUNTRIES)}

# 🤫 瞞天過海的開局公告：100% 抹除任何「第10回合、整蠱、解體、四分五裂」的蛛絲馬跡！
if not st.session_state.game_started:
    st.header("🎮 多人單機熱座模式：請四位玩家分配國家與確認開局特質")
    st.markdown("""
    **📢 歐亞列強開局天賦公告（1936歷史硬核還原）：**
    *   **🔵 中華民國**：【四億同胞】擁有全場最高 **1億可用人力** 且戰損減半！但因為初期國內政治局勢尚未統一，**開局四周被「地方軍閥」色塊所包圍**，前期必須消耗PP下達軍令清除割據，發育腳步需要精打細算！
    *   **💗 大日本帝國**：【軍備發達】開局**自動解鎖步槍與火砲科技**，且倉庫內初始就囤積了 **3萬支先進步槍與800門大砲**，極度適合走早期閃擊戰流派！
    *   **⚫ 德意志國**：【閃擊意志】同日本一樣科技極度發達，開局**自動解鎖步槍與火砲科技**，且初始自帶 **3萬支先進步槍與800門大砲**，擁有全場最頂級的陸軍初始面板加成！
    *   **🔴 蘇聯**：【紅色鋼鐵雄心】極度推薦新手或資深玩家！開局**直接割據右下角 4 格龐大領地**，並自帶高達 **11 座民用工廠**，大後方經濟與資源發育效率高居全歐亞第一，是當之無愧的後期大魔王。
                
    **🔥 外交仇恨與宣戰規則（平衡優化）：**
    *   **歷史宿怨**：開局時，【中華民國】與【大日本帝國】之間的雙向仇恨值起始即為 **50**。中華民國與周邊【地方軍閥】的初始仇恨值亦為 **50**。其餘大國互為 **0**。
    *   **宣戰限制**：對特定強權或地方軍閥的仇恨值**必須達到 100**，方可下達精準突擊戰令，奪取對方的格子！
    *   **戰力平衡**：每位玩家每回合**精準指定突擊限用 1 次**，防止連擊推平，大幅增加戰棋博弈與外交戰略感！
    """)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_roc = st.text_input("🔵 玩家 1 名字（控制：中華民國）", "玩家_1")
        p_ger = st.text_input("⚫ 玩家 2 名字（控制：德意志國）", "玩家_2")
    with col_p2:
        p_jap = st.text_input("💗 玩家 3 名字（控制：大日本帝國）", "玩家_3")
        p_ussr = st.text_input("🔴 玩家 4 名字（控制：蘇聯）", "玩家_4")
        
    if st.button("🚀 分配完畢，大戰正式開打！", type="primary", use_container_width=True):
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
if "soviet_collapsed" not in st.session_state:
    st.session_state.soviet_collapsed = False  

# 使用標準元組解包法安全初始化地圖
if "grid_map" not in st.session_state:
    base_grid = [["中立荒漠" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for row_idx in range(MAP_SIZE):
        for col_idx in range(MAP_SIZE):
            if row_idx == 0 and col_idx == 0:
                base_grid[row_idx][col_idx] = "中華民國"
            elif (row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx == 0) or \
                 (row_idx == 1 and col_idx == 1) or (row_idx == 0 and col_idx == 2) or \
                 (row_idx == 2 and col_idx == 0):
                base_grid[row_idx][col_idx] = "地方軍閥"
            elif row_idx == 0 and col_idx == (MAP_SIZE - 1):
                base_grid[row_idx][col_idx] = "德意志國"
            elif row_idx == (MAP_SIZE - 1) and col_idx == 0:
                base_grid[row_idx][col_idx] = "大日本帝國"
            elif row_idx >= (MAP_SIZE - 2) and col_idx >= (MAP_SIZE - 2):
                base_grid[row_idx][col_idx] = "蘇聯"
    st.session_state.grid_map = base_grid

# 初始化國家獨立數據
if "player_data" not in st.session_state:
    p_data = {}
    for c in COUNTRIES:
        mp = 6000000
        civ = 8
        if c == "中華民國": mp = 100000000
        if c in ["大日本帝國", "德意志國"]: stock_b, stock_a, t_ok = 30000, 800, "✅ 已解鎖"
        else: stock_b, stock_a, t_ok = 5000, 50, "🔒 未研發"
        if c == "蘇聯": civ = 11
        
        animosity = {enemy: 0 for enemy in COUNTRIES if enemy != c}
        if c == "中華民國":
            animosity["大日本帝國"] = 50
            animosity["地方軍閥"] = 50  
        if c == "大日本帝國":
            animosity["中華民國"] = 50
            
        p_data[c] = {
            "pp": 150,
            "manpower": mp,
            "civ_factories": civ,
            "mil_factories": 5,
            "tech": {"中正式步槍": t_ok, "博福斯山砲": t_ok, "中型戰車": "🔒 未研發"},
            "allocation": {"步槍": 3, "火砲": 2, "戰車": 0},
            "stockpile": {"步槍": stock_b, "火砲": stock_a, "戰車": 0},
            "animosity": animosity  
        }
    p_data["地方軍閥"] = {
        "stockpile": {"步槍": 8000, "火砲": 100},
        "animosity": {"中華民國": 50}
    }
    st.session_state.player_data = p_data

if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 歷史日誌：20×20 大棋盤啟動！各方強權已進入臨戰狀態。"]

# 5. 判斷當前玩家與其數據
current_player = COUNTRIES[st.session_state.turn_index]
current_user_name = st.session_state.player_names[current_player]
player_stats = st.session_state.player_data[current_player]

# 6. 頂部資源列 (HUD)
st.subheader(f"👑 目前回合：【{current_user_name}】正在操作 ➔ {current_player} (第 {st.session_state.total_turns} 大回合)")

if current_player == "中華民國":
    st.info("💡 【核心政治限制激活】：你擁有 1 億可用人力且戰損減半！但你的四周已被【地方軍閥（深橘色）】死死堵住，必須先在第3分頁累積仇恨值正式宣戰，才能逐一剿滅並突擊吞併他們！")
elif current_player in ["大日本帝國", "德意志國"]:
    st.success("💡 【軍備大國天賦激活】：你開局就擁有先進的步槍與火砲科技，且倉庫塞滿了現成的高級軍火！")
elif current_player == "蘇聯":
    if st.session_state.soviet_collapsed:
        st.error("🚨 【內戰懲罰】：蘇聯已陷入瘋狂的四分五裂狀態！你的大部分工廠與武器物資已被割據軍閥強行沒收！")
    else:
        st.error("💡 【紅色鋼鐵雄心激活】：你開局就坐擁 4 格核心領土，並自帶高達 11 座民用工廠，經濟與資源累積速度冠絕全場！")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("👑 政治點數 (PP)", f"{player_stats['pp']}")
with col2: st.metric("👥 可用人力", f"{player_stats['manpower']:,}")
with col3: st.metric("🏭 工廠 (民/軍)", f"{player_stats['civ_factories']} / {player_stats['mil_factories']}")
with col4: st.metric("🔫 步槍 / 🍏 火砲庫存", f"{player_stats['stockpile']['步槍']:,} / {player_stats['stockpile']['火砲']:,}")
with col5: st.metric("🚜 戰車庫存", f"{player_stats['stockpile']['戰車']:,} 輛")

st.markdown("---")

# 7. 側邊欄：回合結束與隱藏內戰判定
with st.sidebar:
    st.header("⏱️ 回合制戰略中心")
    st.success(f"👉 請【{current_user_name}】完成決策後結束回合。")
    
    if st.button("🏁 結束本回合 (End Turn)", type="primary", use_container_width=True):
        if player_stats["tech"]["中正式步槍"] == "✅ 已解鎖": 
            player_stats["stockpile"]["步槍"] += player_stats["allocation"]["步槍"] * 800
        if player_stats["tech"]["博福斯山砲"] == "✅ 已解鎖": 
            player_stats["stockpile"]["火砲"] += player_stats["allocation"]["火砲"] * 80
        if player_stats["tech"]["中型戰車"] == "✅ 已解鎖": 
            player_stats["stockpile"]["戰車"] += player_stats["allocation"]["戰車"] * 15
        player_stats["pp"] += 60
        
        st.session_state.turn_index += 1
        if st.session_state.turn_index >= 4:
            st.session_state.turn_index = 0
            st.session_state.total_turns += 1
            
        # 🤫 隱藏內戰定時炸彈
        if st.session_state.total_turns == 10 and not st.session_state.soviet_collapsed:
            temp_map = np.array(st.session_state.grid_map)
            soviet_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if temp_map[r, c] == "蘇聯"]
            
            if soviet_coords:
                np.random.shuffle(soviet_coords)
                chunks = np.array_split(soviet_coords, 4)
                
                for r, c in chunks[0]: temp_map[r, c] = "法西斯蘇聯" 
                for r, c in chunks[1]: temp_map[r, c] = "民主蘇聯"   
                for r, c in chunks[2]: temp_map[r, c] = "君主蘇聯"   
                for r, c in chunks[3]: temp_map[r, c] = "蘇聯"       
                
                st.session_state.grid_map = temp_map.tolist()
                
                sov_data = st.session_state.player_data["蘇聯"]
                sov_data["civ_factories"] = max(1, int(sov_data["civ_factories"] * 0.25))
                sov_data["mil_factories"] = max(1, int(sov_data["mil_factories"] * 0.25))
                sov_data["manpower"] = int(sov_data["manpower"] * 0.25)
                sov_data["stockpile"]["步槍"] = int(sov_data["stockpile"]["步槍"] * 0.25)
                sov_data["stockpile"]["火砲"] = int(sov_data["stockpile"]["火砲"] * 0.25)
                sov_data["stockpile"]["戰車"] = int(sov_data["stockpile"]["戰車"] * 0.25)
                
                st.session_state.soviet_collapsed = True
                st.session_state.battle_log.insert(0, "🚨🚨 歷史震撼事件：蘇維埃二次大內戰引爆！！最高蘇維埃政權瓦解，全境瞬間四分五裂！法西斯白軍、民主黃軍、君主綠軍割據歐亞，原本的共產紅軍痛失 75% 國土與後方軍火庫！！")
        
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
    for log in st.session_state.battle_log[:8]:
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
    if st.session_state.soviet_collapsed:
        st.warning("⚠️ 警告：地圖右下角已進入【蘇聯大解體狀態】，請注意多政權割據戰區！")
        
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            owner = st.session_state.grid_map[row][col]
            color = COLOR_MAP[owner]
rect = plt.Rectangle((col, MAP_SIZE - 1 - row), 1, 1, linewidth=0.5, edgecolor='#222222', facecolor=color, alpha=0.9)ax.add_patch(rect)if owner != "中立荒漠":lbl = owner[:2]if owner == "法西斯蘇聯": lbl = "白蘇"elif owner == "民主蘇聯": lbl = "黃蘇"elif owner == "君主蘇聯": lbl = "綠蘇"ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, lbl, color='black' if color in ['#ffffff', '#ffcc00'] else 'white', ha='center', va='center', fontsize=7, weight='bold')elif (row % 4 == 0 and col % 4 == 0):ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, f"{row+1},{col+1}", color='#ffffff', ha='center', va='center', fontsize=6, alpha=0.15)ax.set_xlim(0, MAP_SIZE)ax.set_ylim(0, MAP_SIZE)ax.set_xticks(range(MAP_SIZE + 1))ax.set_yticks(range(MAP_SIZE + 1))ax.grid(True, color='#222222', linestyle='-', linewidth=0.5)ax.tick_params(colors='white', labelsize=8)st.pyplot(fig)plt.close(fig)# 領土統計st.subheader("📊 全球版圖控制統計")counts = {"中華民國": 0, "德意志國": 0, "大日本帝國": 0, "蘇聯": 0, "地方軍閥": 0, "法西斯蘇聯": 0, "民主蘇聯": 0, "君主蘇聯": 0, "中立荒漠": 0}for r in range(MAP_SIZE):for c in range(MAP_SIZE): counts[st.session_state.grid_map[r][c]] += 1mc1, mc2, mc3, mc4 = st.columns(4)mc1.metric(f"🔵 中華民國", f"{counts['中華民國']} 格")mc2.metric(f"⚫ 德意志國", f"{counts['德意志國']} 格")mc3.metric(f"💗 大日本帝國", f"{counts['大日本帝國']} 格")mc4.metric(f"🔴 共產蘇聯 (玩家)", f"{counts['蘇聯']} 格")st.markdown("---")sc1, sc2, sc3, sc4 = st.columns(4)sc1.metric("🥮 地方割據軍閥", f"{counts['地方軍閥']} 格")if st.session_state.soviet_collapsed:sc2.metric("⚪ 法西斯蘇聯 (NPC)", f"{counts['法西斯蘇聯']} 格")sc3.metric("🟡 民主蘇聯 (NPC)", f"{counts['民主蘇聯']} 格")sc4.metric("🟢 君主蘇聯 (NPC)", f"{counts['君主蘇聯']} 格")--- TAB 2: 科研與產線 ---with tab_tech:st.header(f"🔬 {current_player} 軍工科學院")st.subheader("💡 獨立軍備科研（日德玩家開局已解鎖，其餘玩家需花 PP 研發）")tc1, tc2, tc3 = st.columns(3)with tc1:st.markdown("##### 🔫 中正式步槍 (1936)")rifle_status = player_stats["tech"]["中正式步槍"]if rifle_status == "🔒 未研發" and player_stats["pp"] >= 50:if st.button("🧪 消耗 50 PP 研發輕武器", key="r_tech"):player_stats["pp"] -= 50player_stats["tech"]["中正式步槍"] = "✅ 已解鎖"st.rerun()else:st.write(f"當前狀態: {rifle_status}")with tc2:st.markdown("##### 🍏 博福斯山砲 (1939)")art_status = player_stats["tech"]["博福斯山砲"]if art_status == "🔒 未研發" and player_stats["pp"] >= 100:if st.button("🧪 消耗 100 PP 研發重火砲", key="a_tech"):player_stats["pp"] -= 100player_stats["tech"]["博福斯山砲"] = "✅ 已解鎖"st.rerun()else:st.write(f"當前狀態: {art_status}")with tc3:st.markdown("##### 🚜 中型戰車 (1941)")tank_status = player_stats["tech"]["中型戰車"]if tank_status == "🔒 未研發" and player_stats["pp"] >= 150:if st.button("🧪 消耗 150 PP 研發裝甲裝備", key="t_tech"):player_stats["pp"] -= 150player_stats["tech"]["中型戰車"] = "✅ 已解鎖"st.rerun()else:st.write(f"當前狀態: {tank_status}")st.markdown("---")st.subheader("🏭 本輪軍用工廠產線分配")st.caption(f"你當前總共擁有 {player_stats['mil_factories']} 座軍用工廠。請調配生產權重（總工廠數請勿超過上限）：")current_max_mil = player_stats['mil_factories']safe_alloc_rifle = min(player_stats['allocation']['步槍'], current_max_mil)alloc_rifle = st.number_input("分配給【步槍產線】的工廠數", 0, current_max_mil, safe_alloc_rifle, key="ar")remaining_after_rifle = max(0, current_max_mil - alloc_rifle)safe_alloc_art = min(player_stats['allocation']['火砲'], remaining_after_rifle)alloc_art = st.number_input("分配給【火砲產線】的工廠數", 0, remaining_after_rifle, safe_alloc_art, key="aa")remaining_after_art = max(0, remaining_after_rifle - alloc_art)safe_alloc_tank = min(player_stats['allocation']['戰車'], remaining_after_art)alloc_tank = st.number_input("分配給【戰車產線】的工廠數", 0, remaining_after_art, safe_alloc_tank, key="at")if st.button("⚙️ 儲存本輪產線配置", use_container_width=True):player_stats['allocation']['步槍'] = alloc_rifleplayer_stats['allocation']['火砲'] = alloc_artplayer_stats['allocation']['戰車'] = alloc_tankst.success("⚙️ 軍工生產線配置成功更新！")st.rerun()--- TAB 3: 外交與擴張戰令 ---with tab_action:st.header(f"🎯 【{current_user_name}】的最高統帥部與外交戰令")ac1, ac2 = st.columns(2)with ac1:st.subheader("🛠️ 選項一：精準指定方格突擊（每回合限 1 次）")attack_flag_key = f"attack_used_{st.session_state.total_turns}_{st.session_state.turn_index}"if attack_flag_key not in st.session_state:st.session_state[attack_flag_key] = Falsetarget_row = st.number_input("目標橫列座標 (Row 1-20)", 1, 20, 1, key="tgt_row")target_col = st.number_input("目標縱行座標 (Col 1-20)", 1, 20, 1, key="tgt_col")r_idx = target_row - 1c_idx = target_col - 1current_owner = st.session_state.grid_map[r_idx][c_idx]st.write(f"🔍 目標座標 [{target_row}, {target_col}] 控制者：{current_owner}")is_disabled = st.session_state[attack_flag_key]if is_disabled:st.warning("⚠️ 本回合你已經下達過精準突擊或擴張指令了！請等待下一回合解鎖。")if st.button("⚔️ 下達精準點對點突擊！", type="primary", use_container_width=True, disabled=is_disabled):if current_owner == current_player:st.error("❌ 這是你自己的領土！請選擇其他敵方或中立格子進攻！")elif current_owner in ["法西斯蘇聯", "民主蘇聯", "君主蘇聯"]:st.error("🔒 軍閥限制：該方格為內戰軍閥盤踞地，部隊目前因戰略混亂無法越界進攻這些NPC分裂勢力！")elif current_owner == "中立荒漠":temp_arr = np.array(st.session_state.grid_map)temp_arr[r_idx, c_idx] = current_playerst.session_state.grid_map = temp_arr.tolist()player_stats["civ_factories"] += 1st.session_state.battle_log.insert(0, f"🚩 精準擴張：【{current_user_name}({current_player})】開拓佔領了中立方格 [{target_row}, {target_col}]！")st.session_state[attack_flag_key] = Truest.rerun()else:current_animosity = player_stats["animosity"].get(current_owner, 0)if current_animosity < 100:st.error(f"🔒 外交限制：你對【{current_owner}】的仇恨值目前僅為 {current_animosity} / 100！在仇恨破百正式宣戰前，部隊無法越界搶奪格子！請先至右側製造外交爭端！")else:enemy_name = "地方守軍" if current_owner == "地方軍閥" else st.session_state.player_names[current_owner]enemy_stats = st.session_state.player_data[current_owner]r_bonus = 35 if player_stats["stockpile"]["步槍"] > 5000 else -15a_bonus = 50 if player_stats["stockpile"]["火砲"] > 300 else 0t_bonus = 80 if player_stats["stockpile"]["戰車"] > 20 else 0attack_power = 50 + r_bonus + a_bonus + t_bonus + np.random.randint(-15, 15)enemy_r_bonus = 35 if enemy_stats["stockpile"]["步槍"] > 5000 else -15enemy_a_bonus = 40 if enemy_stats["stockpile"].get("火砲", 0) > 200 else 0defense_power = 60 + enemy_r_bonus + enemy_a_bonus + np.random.randint(-10, 10)player_stats["stockpile"]["步槍"] = max(0, player_stats["stockpile"]["步槍"] - 2500)enemy_stats["stockpile"]["步槍"] = max(0, enemy_stats["stockpile"]["步槍"] - 1800)my_loss = np.random.randint(25000, 75000) if current_player == "中華民國" else np.random.randint(50000, 150000)enemy_loss = np.random.randint(25000, 75000) if current_owner == "中華民國" else np.random.randint(50000, 150000)player_stats["manpower"] = max(0, player_stats["manpower"] - my_loss)if "manpower" in enemy_stats:enemy_stats["manpower"] = max(0, enemy_stats["manpower"] - enemy_loss)if attack_power > defense_power:temp_arr = np.array(st.session_state.grid_map)temp_arr[r_idx, c_idx] = current_playerst.session_state.grid_map = temp_arr.tolist()st.session_state.battle_log.insert(0, f"💥 捷報！【{current_user_name}({current_player})】突破 100 仇恨全面爆發攻勢！成功強奪了【{enemy_name}】的格子 [{target_row}, {target_col}]！")else:st.session_state.battle_log.insert(0, f"🛡️ 戰敗：【{current_user_name}({current_player})】對 [{target_row}, {target_col}] 的強攻被對方死守擊退！")st.session_state[attack_flag_key] = Truest.rerun()with ac2:st.subheader("⚡ 選項二：集團軍拓荒與「外交製造爭端」")st.markdown("##### 📡 統帥部外交部：主動挑釁（提升仇恨值）")provoke_options = [c for c in COUNTRIES if c != current_player]if current_player == "中華民國":provoke_options.append("地方軍閥")provoke_target = st.selectbox("請選擇你要主動挑釁、製造地緣政治摩擦的國家/軍閥：", provoke_options)if st.button(f"🔥 消耗 30 PP 製造爭端，挑釁【{provoke_target}】", use_container_width=True):if player_stats["pp"] >= 30:player_stats["pp"] -= 30gain = np.random.randint(15, 26)player_stats["animosity"][provoke_target] = min(100, player_stats["animosity"][provoke_target] + gain)if provoke_target in st.session_state.player_data:st.session_state.player_data[provoke_target]["animosity"][current_player] = min(100, st.session_state.player_data[provoke_target]["animosity"].get(current_player, 0) + gain)st.session_state.battle_log.insert(0, f"📡 外交挑釁：【{current_user_name}({current_player})】故意尋釁滋事，與【{provoke_target}】的雙向仇恨值暴增 {gain} 點！")st.rerun()else: st.error("❌ 政治點數不足 30 PP！")st.markdown("---")st.markdown("##### 🚀 啟動集團軍：閃擊大範圍拓荒 (消耗 40 PP)")st.caption("隨機吞併 1~5 格中立灰色荒漠。在中原瘋狂擴張的同時，有 35% 機率隨機引爆邊境摩擦，導致隨機大國對你的仇恨度飆升！")if st.button("發動集團軍拓荒！", use_container_width=True):if player_stats["pp"] >= 40:player_stats["pp"] -= 40neutral_coords = []for r in range(MAP_SIZE):for c in range(MAP_SIZE):if st.session_state.grid_map[r][c] == "中立荒漠": neutral_coords.append((r, c))if neutral_coords:conquest_count = min(len(neutral_coords), np.random.randint(1, 6))chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]temp_arr = np.array(st.session_state.grid_map)for r, c in chosen_spots: temp_arr[r, c] = current_playerst.session_state.grid_map = temp_arr.tolist()player_stats["civ_factories"] += conquest_countplayer_stats["stockpile"]["步槍"] += conquest_count * 500st.session_state.battle_log.insert(0, f"⚡ 拓荒：【{current_user_name}({current_player})】擴張吞併了 {conquest_count} 格中立區，工廠產線規模擴大！")if np.random.rand() < 0.35:other_countries = [c for c in COUNTRIES if c != current_player]hit_country = np.random.choice(other_countries)clash_gain = np.random.randint(10, 21)player_stats["animosity"][hit_country] = min(100, player_stats["animosity"][hit_country] + clash_gain)st.session_state.player_data[hit_country]["animosity"][current_player] = min(100, st.session_state.player_data[hit_country]["animosity"][current_player] + clash_gain)st.session_state.battle_log.insert(0, f"💥 邊境擦槍走火！我軍在開拓邊疆時與【{hit_country}】守軍發生零星摩擦，雙方仇恨飆升 {clash_gain} 點！")st.rerun()else:st.error("❌ 全地圖中立荒漠已被瓜分完畢！請改用選項一精準突擊對手領土！")else:st.error("❌ 政治點數不足 40 PP，無法發動集團軍大規模盲擴張！")
