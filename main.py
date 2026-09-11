import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 1. 設置網頁（無痕歷史偽裝，抹除所有整蠱字眼）
st.set_page_config(page_title="Hearts of Grid IV: 大洋海權閃擊戰", page_icon="⚓", layout="wide")
st.title("⚓ Hearts of Grid IV: 歐亞群雄戰紀（100×100 歷史疆域·巨型海戰完全體）")

# 2. 定義核心海陸色彩字典
COUNTRIES = ["中華民國", "德意志第三帝國（納粹德國）", "大日本帝國", "蘇維埃社會主義共和國聯邦（蘇聯）"]
COLOR_MAP = {
    "中華民國": "#003399",  # 藍色 🔵 (秋海棠巨島)
    "德意志第三帝國（納粹德國）": "#222222",  # 黑色 ⚫ (歐陸極盛巨島)
    "大日本帝國": "#ff9999",  # 粉紅色 💗 (上古彌生時代 2x2 袖珍小島)
    "蘇維埃社會主義共和國聯邦（蘇聯）": "#cc0000",      # 正紅色 🔴 (歐亞橫跨巨島)
    "中華蘇維埃反國抗日革命軍": "#990000",  # 鐵血深紅 🩸 (秋海棠島內 1 格星火)
    "中立荒漠島嶼": "#7f8c8d", # 灰色 🟤 (可供爭奪的陸地)
    "太平洋/大西洋深藍大洋": "#0a192f" # 🌊 萬格大洋深藍（海軍遠征交戰區）
}

MAP_SIZE = 100  

# 3. 系統初始化與選國/選人數階段
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_names" not in st.session_state:
    st.session_state.player_names = {c: f"玩家_{i+1}" for i, c in enumerate(COUNTRIES)}
if "is_human" not in st.session_state:
    st.session_state.is_human = {c: True for c in COUNTRIES}

if not st.session_state.game_started:
    st.header("🎮 統帥部召集：請配置真人人數與各大島國海軍指揮官")
    st.markdown("""
    **📢 100×100 海戰完全體版（硬核歷史疆域復刻）戰略公告：**
    全棋盤已被 **10,000 格深藍大洋** 吞併！四大列強以其**「歷史極盛/極小版圖」**孤懸於大洋四角，成為不相連的島國！
    海陸天險徹底切斷陸路，**陸軍僅能作為輔助防守，進攻必須全面依靠海軍跨海遠征**！
    
    **🗺️ 列強地理疆域與海軍天賦（1936硬核考究）：**
    *   **🔵 中華民國**：割據左上角，復刻歷史最大**「秋海棠版圖」**之超大海島！坐擁最高 **1億可用人力**，防守反登陸能力天下第一！
    *   **⚫ 德意志第三帝國（納粹德國）**：割據右上角，復刻 **1942歐洲極盛版圖**島群！初始自帶 **300艘巨砲戰艦與50艘王牌潛艇**，閃擊制海權面板極高！
    *   **🔴 蘇維埃社會主義共和國聯邦（蘇聯）**：割據右下角，復刻**「橫跨歐亞紅色巨熊」**之狹長巨島！自帶 **11 座民用造船廠**，大後方戰艦暴兵效率全場第一。
    *   **💗 大日本帝國**：割據左下角，依歷史指令強制復刻**「上古彌生/古墳時代」最小疆域（僅 2×2 共 4 格彈丸海島）**！【天險優化】：雖然本土極小，但極度難被精準定位突擊！初始倉庫塞滿了 **300艘先進驅逐艦與大批海軍物資**！
    *   **🩸 蘇抗革命軍**：精準保持 **1 格火星**，孤懸於藍色秋海棠島嶼的腹地心臟！與日本自帶 100 回合宿敵宣戰仇恨！
    """)
    
    num_human = st.selectbox("選擇真人玩家人數", [1, 2, 3, 4], index=3)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_roc_human = st.checkbox("🔵 控制中華民國", value=True)
        p_roc_name = st.text_input("🔵 中華民國 海軍總司令名字", "玩家_1")
        p_ger_human = st.checkbox("⚫ 控制德意志第三帝國（納粹德國）", value=(num_human >= 2))
        p_ger_name = st.text_input("⚫ 德意志第三帝國 海軍總司令名字", "玩家_2")
    with col_p2:
        p_jap_human = st.checkbox("💗 控制大日本帝國", value=(num_human >= 3))
        p_jap_name = st.text_input("💗 大日本帝國 海軍總司令名字", "玩家_3")
        p_ussr_human = st.checkbox("🔴 控制蘇維埃社會主義共和國聯邦（蘇聯）", value=(num_human >= 4))
        p_ussr_name = st.text_input("🔴 蘇聯 海軍總司令名字", "玩家_4")
        
    if st.button("⚓ 跨海大艦隊，正式出航！", type="primary", use_container_width=True):
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

# 4. 全域數據防禦性初始化
if "turn_index" not in st.session_state:
    st.session_state.turn_index = 0  
if "total_turns" not in st.session_state:
    st.session_state.total_turns = 1
if "soviet_collapsed" not in st.session_state:
    st.session_state.soviet_collapsed = False  
if "dead_players" not in st.session_state:
    st.session_state.dead_players = []  
if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["📋 遠征日誌：大洋巨型海戰戰場解鎖！各國海軍主力艦隊已拉響臨戰警報。"]

# 5. 🗺️ 歷史極盛疆域海島化：100x100 萬格像素地圖精準雕刻
if "grid_map" not in st.session_state:
    base_grid = [["太平洋/大西洋深藍大洋" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for r in range(MAP_SIZE):
        for c in range(MAP_SIZE):
            # 🔵 中華民國：左上角雕刻巨型「秋海棠葉」島嶼 (最大疆域比例復刻)
            if 2 <= r < 32 and 2 <= c < 38:
                # 簡單模擬秋海棠的圓潤外弧與外蒙古防區
                if not (r < 6 and c < 10) and not (r > 26 and c >= 30):
                    base_grid[r][c] = "中華民國"
            
            # 🩸 中華蘇維埃反國抗日革命軍：精準在秋海棠海島的核心腹地保留 1 格！
            if r == 15 and c == 15:
                base_grid[r][c] = "中華蘇維埃反國抗日革命軍"
                
            # ⚫ 德意志第三帝國：右上角雕刻「1942歐陸擴張極盛」防區海島
            if 2 <= r < 28 and (MAP_SIZE - 35) <= c < (MAP_SIZE - 2):
                if (r + c) % 7 != 0: # 雕刻出破碎的島鏈與海岸防線
                    base_grid[r][c] = "德意志第三帝國（納粹德國）"
            
            # 💗 大日本帝國：左下角精準復刻「上古彌生/古墳時代」最小版圖島（限制只有 2x2 共 4 格！）
            if (MAP_SIZE - 5) <= r < (MAP_SIZE - 3) and 4 <= c < 6:
                base_grid[r][c] = "大日本帝國"
                
            # 🔴 蘇維埃社會主義共和國聯邦：右下角雕刻「橫跨歐亞巨熊」狹長巨型島嶼
            if (MAP_SIZE - 25) <= r < (MAP_SIZE - 2) and (MAP_SIZE - 45) <= c < (MAP_SIZE - 2):
                if r > (MAP_SIZE - 20) or c > (MAP_SIZE - 25): # 刻畫出長條型西伯利亞大防區
                    base_grid[r][c] = "蘇維埃社會主義共和國聯邦（蘇聯）"
                    
            # 🟤 隨機散布一些中立陸地島嶼，作為跨海跳島戰術的跳板
            if base_grid[r][c] == "太平洋/大西洋深藍大洋" and (r % 15 == 0 and c % 15 == 0):
                if 20 <= r <= 80 and 20 <= c <= 80:
                    base_grid[r][c] = "中立荒漠島嶼"
                    
    st.session_state.grid_map = base_grid

# 初始化大洋海戰獨立資源面板
if "player_data" not in st.session_state:
    p_data = {}
    for c in COUNTRIES:
        mp = 8000000
        if c == "中華民國": mp = 100000000
        # 日德開局自動解鎖高級船戰科技
        if c in ["大日本帝國", "德意志第三帝國（納粹德國）"]: 
            dd, bb, cv, t_ok = 350, 80, 5, "✅ 已解鎖"
        else: 
            dd, bb, cv, t_ok = 30, 5, 0, "🔒 未研發"
            
        animosity = {enemy: 0 for enemy in COUNTRIES if enemy != c}
        if c == "中華民國":
            animosity["大日本帝國"] = 50
            animosity["中華蘇維埃反國抗日革命軍"] = 50  
        if c == "大日本帝國":
            animosity["中華民國"] = 50
            animosity["中華蘇維埃反國抗日革命軍"] = 100  # 🌟 滿值宿敵仇恨！
            
        p_data[c] = {
            "pp": 150,
            "manpower": mp,
            "base_civ": 7, 
            "civ_factories": 10,
            "mil_factories": 5, # 轉化為軍艦造船廠
            "tech": {"驅逐艦產線": t_ok, "主力戰艦產線": t_ok, "航空母艦航線": "🔒 未研發"},
            "allocation": {"驅逐艦": 3, "戰艦": 2, "航母": 0},
            "stockpile": {"驅逐艦": dd, "戰艦": bb, "航母": cv},
            "animosity": animosity  
        }
    p_data["中華蘇維埃反國抗日革命軍"] = {
        "stockpile": {"驅逐艦": 5, "戰艦": 0, "航母": 0},
        "animosity": {"中華民國": 50, "大日本帝國": 100}  
    }
    st.session_state.player_data = p_data

# 6. 即時掃描大洋版圖
counts_current = {k: 0 for k in COLOR_MAP.keys()}
for r in range(MAP_SIZE):
    for c in range(MAP_SIZE):
        cell = st.session_state.grid_map[r][c]
        if cell in counts_current:
            counts_current[cell] += 1

for c in COUNTRIES:
    if c in st.session_state.player_data:
        p_stat = st.session_state.player_data[c]
        p_stat["civ_factories"] = p_stat.get("base_civ", 7) + (counts_current.get(c, 0) // 5)
        p_stat["mil_factories"] = 5 + (p_stat["civ_factories"] // 3)

current_player = COUNTRIES[st.session_state.turn_index]
current_user_name = st.session_state.player_names[current_player]
is_human_turn = st.session_state.is_human[current_player]
player_stats = st.session_state.player_data[current_player]

# 🤖 AI 托管遠征與海上巡邏演算法
if not is_human_turn and current_player not in st.session_state.dead_players:
    ai_stat = player_stats
    ai_stat["pp"] += 60
    if ai_stat["pp"] >= 40:
        ai_stat["pp"] -= 40
        # AI 隨機向相鄰的大洋發射巡邏艇，奪取海權
        neutral_sea = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if st.session_state.grid_map[r][c] == "太平洋/大西洋深藍大洋"]
        if neutral_sea:
            cnt = min(len(neutral_sea), np.random.randint(4, 12))
            chosen = [neutral_sea[i] for i in np.random.choice(len(neutral_sea), cnt, replace=False)]
            t_arr = np.array(st.session_state.grid_map)
            for r, c in chosen: t_arr[r, c] = current_player
            st.session_state.grid_map = t_arr.tolist()
            st.session_state.battle_log.insert(0, f"⚓ AI巡邏：【{current_player}】派遣潛艇編隊，將大洋中 {cnt} 格海域劃入其制海權控制範圍！")
    
    st.session_state.turn_index += 1
    if st.session_state.turn_index >= 4:
        st.session_state.turn_index = 0
        st.session_state.total_turns += 1
    st.rerun()

# 7. 頂部大洋資源列 (HUD)
st.subheader(f"⚓ 帝國聯合艦隊旗艦 ➔ 指揮官：【{current_user_name}】正在操作 {current_player} (第 {st.session_state.total_turns} 大回合)")

if current_player in st.session_state.dead_players:
    st.error(f"🚨 【帝國覆滅】：你的本土所有海島已被完全攻陷，主力艦隊全數沉沒！")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("⚓ 政治點數 (PP)", f"{player_stats['pp']}")
with col2: st.metric("👥 可用海軍海員", f"{player_stats['manpower']:,}")
with col3: st.metric("🏭 軍港/造船廠 水位", f"{player_stats['civ_factories']} / {player_stats['mil_factories']}")
with col4: st.metric("🚢 驅逐艦 / 🚢 戰艦庫存", f"{player_stats['stockpile']['驅逐艦']:,} 艘 / {player_stats['stockpile']['戰艦']:,} 艘")
with col5: st.metric("🦅 航空母艦編隊", f"{player_stats['stockpile']['航母']:,} 艘")

st.markdown("---")

# 8. 側邊欄：海戰日誌
with st.sidebar:
    st.header("⏱️ 海戰戰略統帥部")
    if st.button("🏁 結束本輪航線決策 (End Turn)", type="primary", use_container_width=True):
        if current_player not in st.session_state.dead_players:
            player_stats["stockpile"]["驅逐艦"] += player_stats["allocation"]["驅逐艦"] * 10
            player_stats["stockpile"]["戰艦"] += player_stats["allocation"]["戰艦"] * 2
            if player_stats["tech"]["航空母艦航線"] == "✅ 已解鎖":
                player_stats["stockpile"]["航母"] += player_stats["allocation"]["航母"] * 1
            player_stats["pp"] += 60
        st.session_state.turn_index += 1
        if st.session_state.turn_index >= 4:
            st.session_state.turn_index = 0
            st.session_state.total_turns += 1
        st.rerun()

    if st.button("🔄 重置海戰棋盤", type="secondary", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.subheader("📡 外交仇恨矩陣")
    if current_player not in st.session_state.dead_players:
        for enemy, val in player_stats["animosity"].items():
            status = "⚔️ 可爆發海戰" if val >= 100 else "🕊️ 和平中"
            st.write(f"對【{enemy}】：`{val} / 100` ➔ **{status}**")

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
    st.caption("🗺️ 地理格局說明：中華民國、蘇聯、德意志帝國佔據中央龐大歐亞大陸板塊（歷史最大疆域）；大日本帝國被阻隔在左下角太平洋上古孤島，中間橫亙萬格大洋天險！")
    
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
    sc1.metric("🩸 中華蘇維埃反國抗日革命軍（內陸星火）", f"{counts_current['中華蘇維埃反國抗日革命軍']} 格")
    sc2.metric("⚓ 太平洋/大西洋總海域面積", f"{counts_current['太平洋/大西洋海域']} 格")

# --- TAB 2: 科研與產線 ---
with tab_tech:
    st.header(f"🔬 {current_player} 軍工科學院")
    if current_player in st.session_state.dead_players:
        st.error("❌ 你的國家已被滅國，科研與工廠產線全面停擺！")
    else:
        st.subheader("💡 獨立軍備科研（日德開局已解鎖，其餘玩家需花 PP 研發）")
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown("##### 🔫 中正式步槍 (1936)")
            rifle_status = player_stats["tech"]["中正式步槍"]
            if rifle_status == "🔒 未研發" and player_stats["pp"] >= 50:
                if st.button("🧪 消耗 50 PP 研發輕武器", key="r_tech"):
                    player_stats["pp"] -= 50
                    player_stats["tech"]["中正式步槍"] = "✅ 已解鎖"
                    st.rerun()
            else: st.write(f"當前狀態: **{rifle_status}**")
        with tc2:
            st.markdown("##### 🍏 博福斯山砲 (1939)")
            art_status = player_stats["tech"]["博福斯山砲"]
            if art_status == "🔒 未研發" and player_stats["pp"] >= 100:
                if st.button("🧪 消耗 100 PP 研發重火砲", key="a_tech"):
                    player_stats["pp"] -= 100
                    player_stats["tech"]["博福斯山砲"] = "✅ 已解鎖"
                    st.rerun()
            else: st.write(f"當前狀態: **{art_status}**")
        with tc3:
            st.markdown("##### ⚓ 大和級/俾斯麥級海軍核心 (1941)")
            tank_status = player_stats["tech"]["海軍艦艇"]
            if tank_status == "🔒 未研發" and player_stats["pp"] >= 150:
                if st.button("🧪 消耗 150 PP 研發海軍核心科技", key="t_tech"):
                    player_stats["pp"] -= 150
                    player_stats["tech"]["海軍艦艇"] = "✅ 已解鎖"
                    st.rerun()
            else: st.write(f"當前狀態: **{tank_status}**")

        st.markdown("---")
        st.subheader("🏭 本輪軍用工廠與造船廠產線分配")
        current_max_mil = player_stats['mil_factories']
        
        if player_stats['allocation']['步槍'] + player_stats['allocation']['火砲'] + player_stats['allocation']['造船'] > current_max_mil:
            player_stats['allocation']['步槍'] = current_max_mil
            player_stats['allocation']['火砲'] = 0
            player_stats['allocation']['造船'] = 0

        safe_alloc_rifle = min(player_stats['allocation']['步槍'], current_max_mil)
        alloc_rifle = st.number_input("分配給【步槍產線】的工廠數", 0, current_max_mil, safe_alloc_rifle, key=f"ar_{current_player}")
        remaining_after_rifle = max(0, current_max_mil - alloc_rifle)
        safe_alloc_art = min(player_stats['allocation']['火砲'], remaining_after_rifle)
        alloc_art = st.number_input("分配給【火砲產線】的工廠數", 0, remaining_after_rifle, safe_alloc_art, key=f"aa_{current_player}")
        remaining_after_art = max(0, remaining_after_rifle - alloc_art)
        safe_alloc_ship = min(player_stats['allocation']['造船'], remaining_after_art)
        alloc_ship = st.number_input("分配給【海軍造船產線】的船廠數", 0, remaining_after_art, safe_alloc_ship, key=f"at_{current_player}")
        
        if st.button("⚙️ 儲存本輪產線配置", use_container_width=True, key=f"save_mil_{current_player}"):
            player_stats['allocation']['步槍'] = alloc_rifle
            player_stats['allocation']['火砲'] = alloc_art
            player_stats['allocation']['造船'] = alloc_ship
            st.success("⚙️ 海陸軍軍工生產線配置成功更新！")
            st.rerun()

# --- TAB 3: 外交與擴張戰令（海軍走向規劃版） ---
with tab_action:
    st.header(f"🎯 【{current_user_name}】的最高海軍司令部與外交戰令")
    if current_player in st.session_state.dead_players:
        st.error("❌ 你的國家已被滅國，無法下達任何國家級軍令與外交法案！")
    else:
        ac1, ac2 = st.columns(2)
        with ac1:
            st.subheader("🛠️ 選項一：遠洋精準突擊與海軍走向規劃")
            st.caption("🧭 規劃規則：由於日本孤懸海外，各國相隔大洋，你必須規劃一支遠洋艦隊，指派海軍出戰，陸軍（步槍、火砲）僅能作為登陸輔助加成！")
            
            attack_flag_key = f"attack_used_{st.session_state.total_turns}_{st.session_state.turn_index}"
            if attack_flag_key not in st.session_state: st.session_state[attack_flag_key] = False
                
            target_row = st.number_input("目標橫列座標 (Row 1-100)", 1, 100, 1, key="tgt_row")
            target_col = st.number_input("目標縱行座標 (Col 1-100)", 1, 100, 1, key="tgt_col")
            r_idx, c_idx = target_row - 1, target_col - 1
            current_owner = st.session_state.grid_map[r_idx][c_idx]
            st.write(f"🔍 目標座標 `[{target_row}, {target_col}]` 控制者：**{current_owner}**")
            
            # 海軍走向規劃
            navy_route = st.selectbox("⚓ 請規劃遠洋艦隊跨海進攻走向（影響海軍作戰成功率）：", ["🧭 經由第一島鏈向西南閃擊", "🧭 穿越中途島公海大洋切入", "🧭 繞道北方極地冰洋隱蔽奇襲", "🧭 沿近海海岸線進行蛙跳登陸"])
            
            if st.session_state.total_turns <= 5:
                st.info(f"🕊️ 外交條約約束中：目前是第 {st.session_state.total_turns}/5 回合。跨海精準突擊將在「第 6 回合」解鎖！")
                is_disabled = True
            else:
                is_disabled = st.session_state[attack_flag_key]
                if is_disabled: st.warning("⚠️ 本回合你已經下達過突擊指令了！請等待下一回合。")
                
            if st.button("⚓ 下達海軍遠洋突擊法案！", type="primary", use_container_width=True, disabled=is_disabled):
                if current_owner == "太平洋/大西洋海域":
                    st.error("🌊 這是公海海域！無法將大洋據為陸地領土，請精確指定敵方島嶼或大陸色塊！")
                elif current_owner == current_player: 
                    st.error("❌ 這是你自己的領土！請重新規劃走向！")
                elif current_owner in ["法西斯蘇聯", "民主蘇聯", "君主蘇聯"]: 
                    st.error("🔒 該方格目前因戰略混亂無法越界進攻！")
                elif current_owner == "中立荒漠":
                    if player_stats["stockpile"]["海軍舰艇"] < 1:
                        st.error("❌ 跨海拓荒失敗：你的遠洋海軍艦艇庫存為 0！無法護送陸軍跨越海一天險！請先至造船廠生產！")
                    else:
                        player_stats["stockpile"]["海軍舰艇"] = max(0, player_stats["stockpile"]["海軍舰艇"] - 1)
                        temp_arr = np.array(st.session_state.grid_map)
                        temp_arr[r_idx, c_idx] = current_player
                        st.session_state.grid_map = temp_arr.tolist()
                        st.session_state.battle_log.insert(0, f"🚩 遠洋擴張：【{current_user_name}({current_player})】指派海軍護航，成功開拓佔領了沿海/島嶼方格 [{target_row}, {target_col}]！")
                        st.session_state[attack_flag_key] = True
                        st.rerun()
                else:
                    current_animosity = player_stats["animosity"].get(current_owner, 0)
                    if current_animosity < 100: 
                        st.error(f"🔒 外交限制：你對【{current_owner}】的外交仇恨值未滿 100！無法發動全面海戰！")
                    else:
                        if player_stats["stockpile"]["海軍舰艇"] < 5:
                            st.error("❌ 指揮部駁回：跨海進攻敵對政權需要至少 5 艘海軍主力艦艇進行搶灘護航！")
                        else:
                            enemy_name = "蘇抗抗日軍" if current_owner == "中華蘇維埃反國抗日革命軍" else st.session_state.player_names[current_owner]
                            enemy_stats = st.session_state.player_data[current_owner]
                            
                            # 🧮 海軍核心主力對撞演算法
                            route_bonus = np.random.randint(10, 30) if "島鏈" in navy_route or "中途島" in navy_route else np.random.randint(-10, 15)
                            navy_power = player_stats["stockpile"]["海軍舰艇"] * 15 + route_bonus
                            enemy_navy_power = enemy_stats["stockpile"].get("海軍舰艇", 0) * 15
                            
                            # 陸軍輔助加成
                            army_bonus = 25 if player_stats["stockpile"]["步槍"] > 10000 else 0
                            art_bonus = 35 if player_stats["stockpile"]["火砲"] > 500 else 0
                            attack_power = navy_power + army_bonus + art_bonus + np.random.randint(-15, 15)
                            
                            enemy_army_bonus = 20 if enemy_stats["stockpile"]["步槍"] > 10000 else 0
                            defense_power = enemy_navy_power + enemy_army_bonus + 50 + np.random.randint(-10, 10)
                            
                            # ⚓ 戰鬥武器損耗
                            player_stats["stockpile"]["海軍舰艇"] = max(0, player_stats["stockpile"]["海軍舰艇"] - np.random.randint(2, 5))
                            player_stats["stockpile"]["步槍"] = max(0, player_stats["stockpile"]["步槍"] - 2500)
                            if "海軍舰艇" in enemy_stats:
                                enemy_stats["海軍舰艇"] = max(0, enemy_stats["海軍舰艇"] - np.random.randint(1, 4))
                            if "stockpile" in enemy_stats and "步槍" in enemy_stats["stockpile"]:
                                enemy_stats["stockpile"]["步槍"] = max(0, enemy_stats["stockpile"]["步槍"] - 1800)
                            
                            # 人力與戰損結算
                            my_loss = np.random.randint(25000, 75000) if current_player == "中華民國" else np.random.randint(50000, 150000)
                            player_stats["manpower"] = max(0, player_stats["manpower"] - my_loss)
                            
                            if attack_power > defense_power:
                                temp_arr = np.array(st.session_state.grid_map)
                                temp_arr[r_idx, c_idx] = current_player
                                st.session_state.grid_map = temp_arr.tolist()
                                st.session_state.battle_log.insert(0, f"💥 遠洋大捷！【{current_user_name}({current_player})】透過【{navy_route}】規劃成功合圍！艦隊重創敵方，強行登陸奪取了【{enemy_name}】的格子 [{target_row}, {target_col}]！")
                                
                                if current_owner in COUNTRIES:
                                    flat_map = [grid_cell for row_list in st.session_state.grid_map for grid_cell in row_list]
                                    if flat_map.count(current_owner) == 0:
                                        st.session_state.dead_players.append(current_owner)
                                        st.session_state.battle_log.insert(0, f"💀💀 全球震驚：【{enemy_name}({current_owner})】的最後一格陸地領土被完全吞併，國家宣告亡國！！")
                            else:
                                st.session_state.battle_log.insert(0, f"🛡️ 海戰失利：我軍聯合艦隊在【{navy_route}】遭遇強烈攔截，登陸部隊被擊退！")
                            st.session_state[attack_flag_key] = True
                            st.rerun()

        with ac2:
            st.subheader("⚡ 選項二：集團軍島嶼拓荒與「外交製造爭端」")
            st.markdown("##### 📡 統帥部外交部：主動挑釁（提升外交仇恨值）")
            provoke_options = [c for c in COUNTRIES if c != current_player and c not in st.session_state.dead_players]
            if current_player == "中華民國" and "中華蘇維埃反國抗日革命軍" not in st.session_state.dead_players:
                provoke_options.append("中華蘇維埃反國抗日革命軍")
                
            provoke_target = st.selectbox("請選擇你要主動挑釁的國家/軍隊：", provoke_options)
            
            if st.button(f"🔥 消耗 30 PP 製造外交爭端，挑釁【{provoke_target}】", use_container_width=True):
                if player_stats["pp"] >= 30:
                    player_stats["pp"] -= 30
                    gain = np.random.randint(15, 26)
                    player_stats["animosity"][provoke_target] = min(100, player_stats["animosity"][provoke_target] + gain)
                    if provoke_target in st.session_state.player_data:
                        st.session_state.player_data[provoke_target]["animosity"][current_player] = min(100, st.session_state.player_data[provoke_target]["animosity"].get(current_player, 0) + gain)
                    st.session_state.battle_log.insert(0, f"📡 外交挑釁：【{current_user_name}({current_player})】故意尋釁滋事，與【{provoke_target}】的雙向仇恨值暴增 {gain} 點！")
                    st.rerun()
                else:
                    st.error("❌ 政治點數不足 30 PP！")
                    
            st.markdown("---")
            st.markdown("##### 🚀 啟動海軍陸戰隊：閃擊大範圍陸地拓荒 (消耗 40 PP)")
            st.caption("隨機吞併 6~18 格中立陸地荒漠（自動避開公海海域），有 35% 機率引爆島嶼邊境擦槍走火！")
            
            if st.button("發動海軍陸戰隊拓荒！", use_container_width=True):
                if player_stats["pp"] >= 40:
                    if player_stats["stockpile"]["海軍舰艇"] < 3:
                        st.error("❌ 拓荒失敗：大範圍跨島嶼拓荒需要至少 3 艘海軍艦艇提供登陸掩護！")
                    else:
                        player_stats["pp"] -= 40
                        player_stats["stockpile"]["海軍舰艇"] = max(0, player_stats["stockpile"]["海軍舰艇"] - 2)
                        neutral_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if st.session_state.grid_map[r][c] == "中立荒漠"]
                        
                        if neutral_coords:
                            conquest_count = min(len(neutral_coords), np.random.randint(6, 19))
                            chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]
                            
                            temp_arr = np.array(st.session_state.grid_map)
                            for r, c in chosen_spots: 
                                temp_arr[r, c] = current_player
                            st.session_state.grid_map = temp_arr.tolist()
                            
                            st.session_state.battle_log.insert(0, f"⚡ 萬格海拓：【{current_user_name}({current_player})】繞開深海，強行開拓吞併了 {conquest_count} 格中立島嶼/防區！")
                            
                            if np.random.rand() < 0.35:
                                active_enemies = [c for c in COUNTRIES if c != current_player and c not in st.session_state.dead_players]
                                if active_enemies:
                                    hit_country = np.random.choice(active_enemies)
                                    clash_gain = np.random.randint(10, 21)
                                    player_stats["animosity"][hit_country] = min(100, player_stats["animosity"][hit_country] + clash_gain)
                                    st.session_state.player_data[hit_country]["animosity"][current_player] = min(100, st.session_state.player_data[hit_country]["animosity"][current_player] + clash_gain)
                                    st.session_state.battle_log.insert(0, f"💥 島嶼摩擦！我軍在遠洋開拓時與【{hit_country}】巡邏艦隊發生零星交火，雙方仇恨飆升 {clash_gain} 點！")
                            st.rerun()
                        else: 
                            st.error("❌ 全地圖中立陸地已被瓜分完畢！請改用選項一規劃航線突擊對手領土！")
                else: 
                    st.error("❌ 政治點數不足 40 PP！")
