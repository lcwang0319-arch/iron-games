import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 1. 設置網頁（無痕歷史偽裝，抹除所有整蠱字眼）
st.set_page_config(page_title="Hearts of Grid IV: 歐亞群雄戰紀", page_icon="⚔️", layout="wide")
st.title("⚔️ Hearts of Grid IV: 歐亞群雄戰紀（100×100 史詩大洋海陸戰場完全體）")

# 2. 定義四個參戰國家、割據勢力與海洋的核心色彩
COUNTRIES = ["中華民國", "德意志第三帝國（納粹德國）", "大日本帝國", "蘇維埃社會主義共和國聯邦（蘇聯）"]
COLOR_MAP = {
    "中華民國": "#003399",  # 藍色 🔵
    "德意志第三帝國（納粹德國）": "#222222",  # 黑色 ⚫
    "大日本帝國": "#ff9999",  # 粉紅色 💗
    "蘇維埃社會主義共和國聯邦（蘇聯）": "#cc0000",      # 正紅色 🔴
    "中華蘇維埃反國抗日革命軍": "#990000",  # 鐵血深紅 🩸 (開局 1 格核心，與日本宿敵)
    "法西斯蘇聯": "#ffffff",  # 白色 ⚪
    "民主蘇聯": "#ffcc00",    # 黃色 🟡
    "君主蘇聯": "#22aa22",    # 綠色 🟢
    "中立荒漠": "#444444",    # 灰色 🟤
    "太平洋/大西洋海域": "#0e2440" # ⚓ 戰略海洋深藍色
}

# 地圖尺寸：100 × 100 (10,000 格超大棋盤)
MAP_SIZE = 100  

# 3. 系統初始化與選國/選人數階段
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_names" not in st.session_state:
    st.session_state.player_names = {c: f"玩家_{i+1}" for i, c in enumerate(COUNTRIES)}
if "is_human" not in st.session_state:
    st.session_state.is_human = {c: True for c in COUNTRIES}

if not st.session_state.game_started:
    st.header("🎮 遊戲設置：選擇真人玩家人數與分配國家控制權")
    st.markdown("""
    **📢 100×100 海陸完全體版戰略公告：**
    地圖已擴張為 **10,000 格海陸局勢棋盤**！新增了不可跨越的 **【太平洋與大西洋大洋海域】**！
    未被真人選擇的強權將由 **【AI 統帥部】** 託管，圍繞著陸地與海岸線展開瘋狂的戰略擴張！
    
    **📢 歐亞列強開局天賦公告（1936歷史硬核還原）：**
    *   **🔵 中華民國**：【四億同胞】擁有最高 **1億可用人力** 且戰損減半！開局與內陸的「中華蘇維埃反國抗日革命軍」根據地相鄰，發育腳步需要精打細算！
    *   **💗 大日本帝國**：【軍備發達】初始囤積 **3萬支步槍與800門大砲**！**開局割據左下角島嶼防區，四周被太平洋海域包圍，戰略地理位置極其孤立！【🚨 宿敵警報】：對中原內陸的「蘇抗」自帶 100 滿值外交仇恨！**
    *   **⚫ 德意志第三帝國（納粹德國）**：【閃擊意志】開局自帶大量高科技軍火，割據地圖右上角，發育陸軍加成面板極高。
    *   **🔴 蘇維埃社會主義共和國聯邦（蘇聯）**：【紅色鋼鐵雄心】割據地圖右下角大後方，坐擁高達 **11 座民用工廠**，資源累積效率全場第一。
                
    **🔥 外交宣戰、滅國與海洋天險限制：**
    *   **🕊️ 戰前動員期**：**前 5 回合為互不侵犯期**，不可精準突擊，請利用此時大範圍拓荒！
    *   **🌊 海洋天險鎖**：大洋深藍色塊為不可進攻、不可拓荒區！所有突擊指令如果指定到海洋方格，將會被指揮部安全駁回！
    *   **💀 完全滅國機制**：如果某國在棋盤上的【最後一格本土陸地】被突擊奪走，該國將宣告**徹底亡國出局**！
    """)
    
    num_human = st.selectbox("選擇真人玩家人數", [1, 2, 3, 4], index=3)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_roc_human = st.checkbox("🔵 控制中華民國", value=True)
        p_roc_name = st.text_input("🔵 中華民國 玩家名稱", "玩家_1")
        p_ger_human = st.checkbox("⚫ 控制德意志第三帝國（納粹德國）", value=(num_human >= 2))
        p_ger_name = st.text_input("⚫ 德意志第三帝國 玩家名稱", "玩家_2")
    with col_p2:
        p_jap_human = st.checkbox("💗 控制大日本帝國", value=(num_human >= 3))
        p_jap_name = st.text_input("💗 大日本帝國 玩家名稱", "玩家_3")
        p_ussr_human = st.checkbox("🔴 控制蘇維埃社會主義共和國聯邦（蘇聯）", value=(num_human >= 4))
        p_ussr_name = st.text_input("🔴 蘇聯 玩家名稱", "玩家_4")
        
    if st.button("🚀 設置完畢，大戰正式開打！", type="primary", use_container_width=True):
        st.session_state.player_names["中華民國"] = p_roc_name
        st.session_state.player_names["德意志第三帝國（納粹德國）"] = p_ger_name
        st.session_state.player_names["大日本帝國"] = p_jap_name
        st.session_state.player_names["蘇維埃社會主義共和國聯邦（蘇聯）"] = p_ussr_name
        
        st.session_state.is_human["中華民國"] = p_roc_human
        st.session_state.is_human["德意志第三帝國（納粹德國）"] = p_ger_human
        st.session_state.is_human["大日本帝國"] = p_jap_human
        st.session_state.is_human["蘇維埃社會主義共和國聯邦（蘇聯）"] = p_ussr_human
        
        st.session_state.game_started = True
        st.rerun()
    st.stop()

# 4. 變數初始化置頂
if "turn_index" not in st.session_state:
    st.session_state.turn_index = 0  
if "total_turns" not in st.session_state:
    st.session_state.total_turns = 1
if "soviet_collapsed" not in st.session_state:
    st.session_state.soviet_collapsed = False  
if "dead_players" not in st.session_state:
    st.session_state.dead_players = []  
if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 歷史日誌：100×100 海陸大地圖啟動！萬格大洋戰場正式解鎖。"]

# 初始化 100x100 大地圖
if "grid_map" not in st.session_state:
    base_grid = [["中立荒漠" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for r_idx in range(MAP_SIZE):
        for c_idx in range(MAP_SIZE):
            if (35 <= r_idx <= 65) or (35 <= c_idx <= 55 and r_idx > 30):
                if not (r_idx < 15 and c_idx >= 80) and not (r_idx >= 80 and c_idx >= 80) and not (r_idx >= 80 and c_idx < 20):
                    base_grid[r_idx][c_idx] = "太平洋/大西洋海域"
            
            if r_idx < 15 and c_idx < 15:
                base_grid[r_idx][c_idx] = "中華民國"
            elif r_idx == 0 and c_idx == 15:
                base_grid[r_idx][c_idx] = "中華蘇維埃反國抗日革命軍"
            elif r_idx < 15 and c_idx >= (MAP_SIZE - 15):
                base_grid[r_idx][c_idx] = "德意志第三帝國（納粹德國）"
            elif r_idx == (MAP_SIZE - 1) and c_idx == 0:
                base_grid[r_idx][c_idx] = "大日本帝國"
            elif r_idx >= (MAP_SIZE - 15) and c_idx >= (MAP_SIZE - 15):
                base_grid[r_idx][c_idx] = "蘇維埃社會主義共和國聯邦（蘇聯）"
    st.session_state.grid_map = base_grid

# 初始化國家數據
if "player_data" not in st.session_state:
    p_data = {}
    for c in COUNTRIES:
        mp = 6000000
        if c == "中華民國": mp = 100000000
        if c in ["大日本帝國", "德意志第三帝國（納粹德國）"]: stock_b, stock_a, t_ok = 30000, 800, "✅ 已解鎖"
        else: stock_b, stock_a, t_ok = 5000, 50, "🔒 未研發"
            
        animosity = {enemy: 0 for enemy in COUNTRIES if enemy != c}
        if c == "中華民國":
            animosity["大日本帝國"] = 50
            animosity["中華蘇維埃反國抗日革命軍"] = 50  
        if c == "大日本帝國":
            animosity["中華民國"] = 50
            animosity["中華蘇維埃反國抗日革命軍"] = 100  
            
        p_data[c] = {
            "pp": 150,
            "manpower": mp,
            "base_civ": 7, 
            "civ_factories": 8 if c != "蘇維埃社會主義共和國聯邦（蘇聯）" else 11,
            "mil_factories": 5,
            "tech": {"中文武器自行研發" if "中正式步槍" not in ["中正式步槍"] else "中正式步槍": t_ok, "中正式步槍": t_ok, "博福斯山砲": t_ok, "海軍艦艇": "🔒 未研發" if c != "大日本帝國" else "✅ 已解鎖"},
            "allocation": {"步槍": 3, "火砲": 2, "造船": 0},
            "stockpile": {"步槍": stock_b, "火砲": stock_a, "海軍艦艇": 5 if c == "大日本帝國" else 1},
            "animosity": animosity  
        }
    p_data["中華蘇維埃反國抗日革命軍"] = {
        "stockpile": {"步槍": 8000, "火砲": 100, "海軍艦艇": 0},
        "animosity": {"中華民國": 50, "大日本帝國": 100}  
    }
    st.session_state.player_data = p_data

# 5. 🛠️ 修正掃描範圍：將原本死寫 20 的限制，全部動態切換為真正的 MAP_SIZE 🛠️
counts_current = {"中華民國": 0, "德意志第三帝國（納粹德國）": 0, "大日本帝國": 0, "蘇維埃社會主義共和國聯邦（蘇聯）": 0, "中華蘇維埃反國抗日革命軍": 0, "法西斯蘇聯": 0, "民主蘇聯": 0, "君主蘇聯": 0, "中立荒漠": 0, "太平洋/大西洋海域": 0}
for r in range(MAP_SIZE):
    for c in range(MAP_SIZE):
        owner_name = st.session_state.grid_map[r][c]
        if owner_name in counts_current:
            counts_current[owner_name] += 1

for c in COUNTRIES:
    if c in st.session_state.player_data:
        p_stat = st.session_state.player_data[c]
        grid_count = counts_current.get(c, 0)
        p_stat["civ_factories"] = p_stat.get("base_civ", 7) + grid_count
        p_stat["mil_factories"] = 5 + (p_stat["civ_factories"] // 3)

# 輪替判定
current_player = COUNTRIES[st.session_state.turn_index]
current_user_name = st.session_state.player_names[current_player]
is_current_human = st.session_state.is_human[current_player]
player_stats = st.session_state.player_data[current_player]

# 🤖 若當前為 AI 托管回合，自動執行 AI 動作並直接跳過
if not is_current_human and current_player not in st.session_state.dead_players:
    ai_stat = player_stats
    ai_stat["pp"] += 60
    if ai_stat["pp"] >= 40:
        ai_stat["pp"] -= 40
        neutral_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if st.session_state.grid_map[r][c] == "中立荒漠"]
        if neutral_coords:
            cnt = min(len(neutral_coords), np.random.randint(6, 18))
            chosen = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), cnt, replace=False)]
            t_arr = np.array(st.session_state.grid_map)
            for r, c in chosen: 
                if 0 <= r < MAP_SIZE and 0 <= c < MAP_SIZE:
                    t_arr[r, c] = current_player
            st.session_state.grid_map = t_arr.tolist()
            st.session_state.battle_log.insert(0, f"🤖 AI戰略：【{current_player}】向內陸狂飆推進，佔領了 {cnt} 格陸地中立防區！")
    
    st.session_state.turn_index += 1
    if st.session_state.turn_index >= 4:
        st.session_state.turn_index = 0
        st.session_state.total_turns += 1
    st.rerun()

# 6. 頂部資源列 (HUD)
mode_label = "👤 真人玩家操作" if is_current_human else "🤖 AI 自動托管中"
st.subheader(f"👑 目前回合：【{current_user_name}】({mode_label}) ➔ {current_player} (第 {st.session_state.total_turns} 大回合)")

if current_player in st.session_state.dead_players:
    st.error(f"🚨 【亡國通報】：【{current_user_name}】的 {current_player} 已被完全吞併消滅！你已失去行動主權！")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("👑 政治點數 (PP)", f"{player_stats['pp']}")
with col2: st.metric("👥 可用人力", f"{player_stats['manpower']:,}")
with col3: st.metric("🏭 工廠 (民/軍)", f"{player_stats['civ_factories']} / {player_stats['mil_factories']}")
with col4: st.metric("🔫 步槍 / 🍏 火砲庫存", f"{player_stats['stockpile'].get('步槍', 0):,} / {player_stats['stockpile'].get('火砲', 0):,}")
with col5: st.metric("⚓ 海軍艦艇庫存", f"{player_stats['stockpile'].get('海軍艦艇', 0):,} 艘")

st.markdown("---")

# 7. 側邊欄
with st.sidebar:
    st.header("⏱️ 回合制戰略中心")
    if current_player in st.session_state.dead_players:
        st.warning("🏳️ 國家已不存在")
    else:
        st.success(f"👉 請【{current_user_name}】進行決策。")
    
    if st.button("🏁 結束本回合 (End Turn)", type="primary", use_container_width=True):
        if current_player not in st.session_state.dead_players:
            if player_stats["tech"]["中正式步槍"] == "✅ 已解鎖": 
                player_stats["stockpile"]["步槍"] = player_stats["stockpile"].get("步槍", 0) + player_stats["allocation"]["步槍"] * 800
            if player_stats["tech"]["博福斯山砲"] == "✅ 已解鎖": 
                player_stats["stockpile"]["火砲"] = player_stats["stockpile"].get("火砲", 0) + player_stats["allocation"]["火砲"] * 80
            if player_stats["tech"]["海軍艦艇"] == "✅ 已解鎖":
                player_stats["stockpile"]["海軍艦艇"] = player_stats["stockpile"].get("海軍艦艇", 0) + player_stats["allocation"]["造船"] * 2
            player_stats["pp"] += 60
        
        st.session_state.turn_index += 1
        if st.session_state.turn_index >= 4:
            st.session_state.turn_index = 0
            st.session_state.total_turns += 1
            
        # 🤫 隱藏內戰定時炸彈：若蘇聯存活，第 10 大回合跳出瞬間自動分裂！
        if st.session_state.total_turns == 10 and not st.session_state.soviet_collapsed and "蘇維埃社會主義共和國聯邦（蘇聯）" not in st.session_state.dead_players:
            temp_map = np.array(st.session_state.grid_map)
            soviet_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if temp_map[r, c] == "蘇維埃社會主義共和國聯邦（蘇聯）"]
            if soviet_coords:
                np.random.shuffle(soviet_coords)
                chunks = np.array_split(soviet_coords, 4)
                if len(chunks) > 0:
                    for coord in chunks: temp_map[coord, coord] = "法西斯蘇聯" 
                if len(chunks) > 1:
                    for coord in chunks: temp_map[coord, coord] = "民主蘇聯"   
                if len(chunks) > 2:
                    for coord in chunks: temp_map[coord, coord] = "君主蘇聯"   
                st.session_state.grid_map = temp_map.tolist()
                
                sov_data = st.session_state.player_data["蘇維埃社會主義共和國聯邦（蘇聯）"]
                sov_data["base_civ"] = max(1, int(sov_data["base_civ"] * 0.25))
                sov_data["manpower"] = int(sov_data["manpower"] * 0.25)
                sov_data["stockpile"]["步槍"] = int(sov_data["stockpile"].get("步槍", 0) * 0.25)
                sov_data["stockpile"]["火砲"] = int(sov_data["stockpile"].get("火砲", 0) * 0.25)
                st.session_state.soviet_collapsed = True
                st.session_state.battle_log.insert(0, f"🚨🚨 歷史震撼事件：蘇聯突發爆發全面大內戰！國土全面割據崩潰！")
        st.rerun()

    if st.button("🔄 重新整場遊戲（返回選國）", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("📡 外交仇恨矩陣")
    if current_player not in st.session_state.dead_players:
        for enemy, val in player_stats["animosity"].items():
            status = "⚔️ 可爆發海戰" if val >= 100 else "🕊️ 和平中"
            st.write(f"對【{enemy}】：`{val} / 100` ➔ **{status}**")
    else:
        st.write("🏳️ 國家已不存在，外交仇恨矩陣關閉。")

    st.markdown("---")
    st.subheader("📜 歐亞前線戰報")
    for log in st.session_state.battle_log[:8]:
        st.caption(log)

# 8. 主畫面分頁
tab_map, tab_tech, tab_action = st.tabs([
    "🗺️ 史詩海陸版圖 (Tactical Board)", 
    "🔬 專屬軍備科研與產線 (Research & Production)", 
    "🎯 戰略專攻與外交戰令 (Military Orders)"
])

# --- TAB 1: 地圖渲染（萬格海陸高效率畫板） ---
with tab_map:
    st.header("🗺️ 100×100 巨型大洋割據防區圖 (10,000格海陸像素矩陣)")
    
    color_keys = list(COLOR_MAP.keys())
    color_to_idx = {k: i for i, k in enumerate(color_keys)}
    
    data_matrix = np.zeros((MAP_SIZE, MAP_SIZE))
    for r in range(MAP_SIZE):
        for c in range(MAP_SIZE):
            data_matrix[r, c] = color_to_idx[st.session_state.grid_map[r][c]]
            
    hex_colors = [COLOR_MAP[k] for k in color_keys]
    custom_cmap = mcolors.ListedColormap(hex_colors)
    
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#1e1e1e')
    ax.imshow(data_matrix, cmap=custom_cmap, origin='upper', interpolation='nearest')
    ax.set_axis_off()
    st.pyplot(fig)
    plt.close(fig)
    
    st.subheader("📊 全球版圖控制統計")
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("🔵 中華民國" + (" (已亡國)" if "中華民國" in st.session_state.dead_players else ""), f"{counts_current['中華民國']} 格")
    mc2.metric("⚫ 德意志第三帝國" + (" (已亡國)" if "德意志第三帝國（納粹德國）" in st.session_state.dead_players else ""), f"{counts_current['德意志第三帝國（納粹德國）']} 格")
    mc3.metric("💗 大日本帝國" + (" (已亡國)" if "大日本帝國" in st.session_state.dead_players else ""), f"{counts_current['大日本帝國']} 格")
    mc4.metric("🔴 蘇維埃聯邦" + (" (已亡國)" if "蘇維埃社會主義共和國聯邦（蘇聯）" in st.session_state.dead_players else ""), f"{counts_current['蘇維埃社會主義共和國聯邦（蘇聯）']} 格")
    
    st.markdown("---")
    sc1, sc2 = st.columns(2)
    sc1.metric("🩸 中華蘇維埃反國抗日革命軍（星火）", f"{counts_current['中華蘇維埃反國抗日革命軍']} 格")
    sc2.metric("⚓ 太平洋/大西洋總海域面積", f"{counts_current['太平洋/大西洋海域']} 格")

# --- TAB 2: 科研與產線 ---
with tab_tech:
    st.header(f"🔬 {current_player} 軍工科學院")
    if current_player in st.session_state.dead_players:
        st.error("❌ 你的國家已被滅國，科研與工廠產線全面停擺！")
    else:
        tc1, tc2, tc3 = st.columns(3)
        with tc1: st.write(f"步槍科技: **{player_stats['tech'].get('中正式步槍', '🔒 未研發')}**")
        with tc2: st.write(f"火砲科技: **{player_stats['tech'].get('博福斯山砲', '🔒 未研發')}**")
        with tc3: 
            st.write(f"海軍研發: **{player_stats['tech'].get('海軍艦艇', '🔒 未研發')}**")
            if player_stats["tech"].get("海軍艦艇", "🔒 未研發") == "🔒 未研發" and player_stats["pp"] >= 100:
                if st.button("🧪 消耗 100 PP 解鎖造船船塢", key=f"unlock_dock_{current_player}"):
                    player_stats["pp"] -= 100
                    player_stats["tech"]["海軍艦艇"] = "✅ 已解鎖"
                    st.rerun()
        
        st.markdown("---")
        st.subheader("🏭 本輪軍用工廠與造船廠產線分配")
        current_max_mil = player_stats['mil_factories']
        alloc_rifle = st.number_input("分配給【步槍產線】的工廠數", 0, current_max_mil, min(player_stats['allocation'].get('步槍', 0), current_max_mil), key=f"ar_{current_player}")
        remaining = max(0, current_max_mil - alloc_rifle)
        alloc_ship = st.number_input("分配給【造船產線】的工廠數", 0, remaining, min(player_stats['allocation'].get('造船', 0), remaining), key=f"as_{current_player}")
        
        if st.button("⚙️ 儲存產線配置", use_container_width=True, key=f"save_mil_{current_player}"):
            player_stats['allocation']['步槍'] = alloc_rifle
            player_stats['allocation']['造船'] = alloc_ship
            st.success("⚙️ 軍工配置成功更新！")
            st.rerun()

# --- TAB 3: 外交與擴張戰令 ---
with tab_action:
    st.header(f"🎯 【{current_user_name}】的外交與最高戰令")
    if current_player in st.session_state.dead_players:
        st.error("❌ 你的國家已被滅國")
    else:
        ac1, ac2 = st.columns(2)
        with ac1:
            st.subheader("🛠️ 選項一：遠洋精準突擊與海軍航線走向規劃")
            attack_flag_key = f"attack_used_{st.session_state.total_turns}_{st.session_state.turn_index}"
            if attack_flag_key not in st.session_state: st.session_state[attack_flag_key] = False
                
            target_row = st.number_input("目標橫列座標 (Row 1-100)", 1, 100, 1, key="tgt_row")
            target_col = st.number_input("目標縱行座標 (Col 1-100)", 1, 100, 1, key="tgt_col")
            r_idx, c_idx = target_row - 1, target_col - 1
            
            if 0 <= r_idx < MAP_SIZE and 0 <= c_idx < MAP_SIZE:
                current_owner = st.session_state.grid_map[r_idx][c_idx]
            else:
                current_owner = "太平洋/大西洋海域"
                
            st.write(f"🔍 目標 `[{target_row}, {target_col}]` 控制者：**{current_owner}**")
            navy_route = st.selectbox("⚓ 請規劃遠洋艦隊跨海進攻走向：", ["🧭 經由第一島鏈向西南閃擊", "🧭 穿越中途島公海大洋切入", "🧭 繞道北方極地冰洋隱蔽奇襲", "🧭 沿近海海岸線進行蛙跳登陸"])
            
            is_disabled = st.session_state[attack_flag_key] if st.session_state.total_turns > 5 else True
            if st.session_state.total_turns <= 5: st.info("🕊️ 前 5 回合和平保護中！第 6 回合解鎖跨陸強攻！")
                
            if st.button("⚔️ 下達遠洋突擊登陸法案！", type="primary", use_container_width=True, disabled=is_disabled):
                if current_owner == "太平洋/大西洋海域":
                    st.error("🌊 這是公海海域！無法收復為陸地。")
                elif current_owner == current_player: 
                    st.error("❌ 這是你自己的領土！")
                elif current_owner == "中立荒漠":
                    if player_stats["stockpile"].get("海軍艦艇", 0) < 1:
                        st.error("❌ 跨海失敗：需要至少 1 艘海軍艦艇提供跨洋運輸與護航！")
                    else:
                        player_stats["stockpile"]["海軍艦艇"] = max(0, player_stats["stockpile"].get("海軍艦艇", 0) - 1)
                        temp_arr = np.array(st.session_state.grid_map)
                        temp_arr[r_idx, c_idx] = current_player
                        st.session_state.grid_map = temp_arr.tolist()
                        st.session_state.battle_log.insert(0, f"🚩 遠洋開拓：【{current_user_name}】指派海軍護航，沿【{navy_route}】成功擴張佔領方格 [{target_row}, {target_col}]！")
                        st.session_state[attack_flag_key] = True
                        st.rerun()
                else:
                    current_animosity = player_stats["animosity"].get(current_owner, 0)
                    if current_animosity < 100: 
                        st.error(f"🔒 外交限制：仇恨值未滿 100，無法跨越公海防區向對手宣戰！")
                    else:
                        if player_stats["stockpile"].get("海軍艦艇", 0) < 3:
                            st.error("❌ 聯合參謀部駁回：跨海進攻敵對據點需要至少 3 艘海軍主力艦搶灘！")
                        else:
                            enemy_name = "抗日革命軍" if current_owner == "中華蘇維埃反國抗日革命軍" else st.session_state.player_names[current_owner]
                            enemy_stats = st.session_state.player_data[current_owner]
                            
                            route_bonus = np.random.randint(10, 30) if "島鏈" in navy_route or "中途島" in navy_route else np.random.randint(-10, 15)
                            navy_power = player_stats["stockpile"].get("海軍艦艇", 0) * 15 + route_bonus
                            enemy_navy_power = enemy_stats["stockpile"].get("海軍艦艇", 0) * 15
                            
                            attack_power = navy_power + 30 + np.random.randint(-15, 15)
                            defense_power = enemy_navy_power + 50 + np.random.randint(-10, 10)
                            
                            player_stats["stockpile"]["海軍艦艇"] = max(0, player_stats["stockpile"].get("海軍艦艇", 0) - 2)
                            if "stockpile" in enemy_stats and "海軍艦艇" in enemy_stats["stockpile"]:
                                enemy_stats["stockpile"]["海軍艦艇"] = max(0, enemy_stats["stockpile"]["海軍艦艇"] - 1)
                            
                            if attack_power > defense_power:
                                temp_arr = np.array(st.session_state.grid_map)
                                temp_arr[r_idx, c_idx] = current_player
                                st.session_state.grid_map = temp_arr.tolist()
                                st.session_state.battle_log.insert(0, f"💥 遠洋大捷！【{current_user_name}】指派海軍經【{navy_route}】重創敵軍，強行登陸奪取方格 [{target_row}, {target_col}]！")
                                
                                if current_owner in COUNTRIES:
                                    flat_map = [grid_cell for row_list in st.session_state.grid_map for grid_cell in row_list]
                                    if flat_map.count(current_owner) == 0:
                                        st.session_state.dead_players.append(current_owner)
                                        st.session_state.battle_log.insert(0, f"💀💀 全球震驚：【{enemy_name}({current_owner})】最後一格陸地淪陷，國家宣告亡國出局！！")
                            else:
                                st.session_state.battle_log.insert(0, f"🛡️ 海戰失利：我軍在【{navy_route}】遭遇強力阻擊，登陸部隊被擊退！")
                            st.session_state[attack_flag_key] = True
                            st.rerun()

        with ac2:
            st.subheader("⚡ 選項二：海軍陸戰隊島嶼拓荒與「外交製造爭端」")
            provoke_options = [c for c in COUNTRIES if c != current_player and c not in st.session_state.dead_players]
            if current_player == "中華民國" and "中華蘇維埃反國抗日革命軍" not in st.session_state.dead_players: provoke_options.append("中華蘇維埃反國抗日革命軍")
            provoke_target = st.selectbox("挑釁目標：", provoke_options, key=f"provoke_sel_{current_player}")
            
            if st.button(f"🔥 製造爭端，挑釁【{provoke_target}】", use_container_width=True, key=f"provoke_btn_{current_player}"):
                if player_stats["pp"] >= 30:
                    player_stats["pp"] -= 30
                    gain = np.random.randint(15, 26)
                    player_stats["animosity"][provoke_target] = min(100, player_stats["animosity"][provoke_target] + gain)
                    st.session_state.battle_log.insert(0, f"📡 外交尋釁：【{current_player}】故意挑釁【{provoke_target}】，雙向仇恨暴增 {gain}！")
                    st.rerun()
                else: st.error("❌ 政治點數不足！")
                    
            st.markdown("---")
            if st.button("🚀 發動海軍陸戰隊大範圍跨島閃擊拓荒！", use_container_width=True, key=f"amphibious_btn_{current_player}"):
                if player_stats["pp"] >= 40:
                    if player_stats["stockpile'].get("海軍艦艇", 0) < 3:
                        st.error("❌ 拓荒失敗：海軍陸戰隊大範圍搶灘登陸，需要至少 3 艘海軍艦艇掩護！")
                    else:
                        player_stats["pp"] -= 40
                        player_stats["stockpile"]["海軍艦艇"] = max(0, player_stats["stockpile"].get("海軍艦艇", 0) - 2)
                        neutral_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if st.session_state.grid_map[r][c] == "中立荒漠"]
                        if neutral_coords:
                            conquest_count = min(len(neutral_coords), np.random.randint(6, 19))
                            chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]
                            temp_arr = np.array(st.session_state.grid_map)
                            for r, c in chosen_spots: 
                                if 0 <= r < MAP_SIZE and 0 <= c < MAP_SIZE:
                                    temp_arr[r, c] = current_player
                            st.session_state.grid_map = temp_arr.tolist()
                            st.session_state.battle_log.insert(0, f"⚡ 萬格海拓：【{current_player}】由海軍陸戰隊護航，一口氣瘋狂吞併開拓了 {conquest_count} 格中立陸地/島嶼！")
                            st.rerun()
