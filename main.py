# --- TAB 3: 外交與擴張戰令 ---
with tab_action:
    st.header(f"🎯 【{current_user_name}】的最高統帥部與外交戰令")
    if current_player in st.session_state.dead_players:
        st.error("❌ 你的國家已被滅國，無法下達 any 國家級軍令與外交法案！")
    else:
        ac1, ac2 = st.columns(2)
        with ac1:
            st.subheader("🛠️ 選項一：精準指定方格突擊（每回合限 1 次）")
            attack_flag_key = f"attack_used_{st.session_state.total_turns}_{st.session_state.turn_index}"
            if attack_flag_key not in st.session_state: st.session_state[attack_flag_key] = False
                
            target_row = st.number_input("目標橫列座標 (Row 1-20)", 1, 20, 1, key="tgt_row")
            target_col = st.number_input("目標縱行座標 (Col 1-20)", 1, 20, 1, key="tgt_col")
            r_idx, c_idx = target_row - 1, target_col - 1
            current_owner = st.session_state.grid_map[r_idx][c_idx]
            st.write(f"🔍 目標座標 `[{target_row}, {target_col}]` 控制者：**{current_owner}**")
            
            if st.session_state.total_turns <= 5:
                st.info(f"🕊️ 外交條約約束中：目前是第 {st.session_state.total_turns}/5 回合。精準突擊將在「第 6 回合」解鎖！")
                is_disabled = True
            else:
                is_disabled = st.session_state[attack_flag_key]
                if is_disabled: st.warning("⚠️ 本回合你已經下達過精準突擊指令了！請等待下一回合解鎖。")
                
            if st.button("⚔️ 下達精準點對點突擊！", type="primary", use_container_width=True, disabled=is_disabled):
                if current_owner == current_player: st.error("❌ 這是你自己的領土！請選擇其他格子進攻！")
                elif current_owner in ["法西斯蘇聯", "民主蘇聯", "君主蘇聯"]: st.error("🔒 軍閥限制：該方格目前因戰略混亂無法越界進攻！")
                elif current_owner == "中立荒漠":
                    temp_arr = np.array(st.session_state.grid_map)
                    temp_arr[r_idx, c_idx] = current_player
                    st.session_state.grid_map = temp_arr.tolist()
                    st.session_state.battle_log.insert(0, f"🚩 精準擴張：【{current_user_name}({current_player})】開拓佔領了中立方格 [{target_row}, {target_col}]！")
                    st.session_state[attack_flag_key] = True
                    st.rerun()
                else:
                    current_animosity = player_stats["animosity"].get(current_owner, 0)
                    if current_animosity < 100: st.error(f"🔒 外交限制：你對【{current_owner}】的仇恨值目前僅為 {current_animosity} / 100！請先至右側製造外交爭端！")
                    else:
                        enemy_name = "抗日革命軍" if current_owner == "中華蘇維埃反國抗日革命軍" else st.session_state.player_names[current_owner]
                        enemy_stats = st.session_state.player_data[current_owner]
                        
                        r_bonus = 35 if player_stats["stockpile"]["步槍"] > 5000 else -15
                        a_bonus = 50 if player_stats["stockpile"]["火砲"] > 300 else 0
                        t_bonus = 80 if player_stats["stockpile"]["戰車"] > 20 else 0
                        attack_power = 50 + r_bonus + a_bonus + t_bonus + np.random.randint(-15, 15)
                        
                        enemy_r_bonus = 35 if enemy_stats["stockpile"]["步槍"] > 5000 else -15
                        enemy_a_bonus = 40 if enemy_stats["stockpile"].get("火砲", 0) > 200 else 0
                        defense_power = 60 + enemy_r_bonus + enemy_a_bonus + np.random.randint(-10, 10)
                        
                        player_stats["stockpile"]["步槍"] = max(0, player_stats["stockpile"]["步槍"] - 2500)
                        enemy_stats["stockpile"]["步槍"] = max(0, enemy_stats["stockpile"]["步槍"] - 1800)
                        
                        my_loss = np.random.randint(25000, 75000) if current_player == "中華民國" else np.random.randint(50000, 150000)
                        enemy_loss = np.random.randint(25000, 75000) if current_owner == "中華民國" else np.random.randint(50000, 150000)
                        player_stats["manpower"] = max(0, player_stats["manpower"] - my_loss)
                        if "manpower" in enemy_stats: enemy_stats["manpower"] = max(0, enemy_stats["manpower"] - enemy_loss)
                        
                        if attack_power > defense_power:
                            temp_arr = np.array(st.session_state.grid_map)
                            temp_arr[r_idx, c_idx] = current_player
                            st.session_state.grid_map = temp_arr.tolist()
                            st.session_state.battle_log.insert(0, f"💥 捷報！【{current_user_name}({current_player})】突破 100 仇恨全面爆發攻勢！成功強奪了【{enemy_name}】的格子 [{target_row}, {target_col}]！")
                            
                            if current_owner in COUNTRIES:
                                flat_map = [grid_cell for row_list in st.session_state.grid_map for grid_cell in row_list]
                                if flat_map.count(current_owner) == 0:
                                    st.session_state.dead_players.append(current_owner)
                                    st.session_state.battle_log.insert(0, f"💀💀 全球震驚：【{enemy_name}({current_owner})】領土被完全吞併，國家宣告亡國！！")
                        else: st.session_state.battle_log.insert(0, f"🛡️ 戰敗：【{current_user_name}({current_player})】對 [{target_row}, {target_col}] 的強攻被擊退！")
                        st.session_state[attack_flag_key] = True
                        st.rerun()

        with ac2:
            st.subheader("⚡ 選項二：集團軍拓荒與「外交製造爭端」")
            st.markdown("##### 📡 統帥部外交部：主動挑釁（提升仇恨值）")
            provoke_options = [c for c in COUNTRIES if c != current_player and c not in st.session_state.dead_players]
            if current_player == "中華民國" and "中華蘇維埃反國抗日革命軍" not in st.session_state.dead_players: provoke_options.append("中華蘇維埃反國抗日革命軍")
            provoke_target = st.selectbox("請選擇你要主動挑釁的國家/軍隊：", provoke_options)
            
            if st.button(f"🔥 消耗 30 PP 製造爭端，挑釁【{provoke_target}】", use_container_width=True):
                if player_stats["pp"] >= 30:
                    player_stats["pp"] -= 30
                    gain = np.random.randint(15, 26)
                    player_stats["animosity"][provoke_target] = min(100, player_stats["animosity"][provoke_target] + gain)
                    if provoke_target in st.session_state.player_data:
                        st.session_state.player_data[provoke_target]["animosity"][current_player] = min(100, st.session_state.player_data[provoke_target]["animosity"].get(current_player, 0) + gain)
                    st.session_state.battle_log.insert(0, f"📡 外交挑釁：【{current_user_name}({current_player})】故意尋釁滋事，與【{provoke_target}】的雙向仇恨值暴增 {gain} 點！")
                    st.rerun()
                else: st.error("❌ 政治點數不足 30 PP！")
                    
            st.markdown("---")
            st.markdown("##### 🚀 啟動集團軍：閃擊大範圍拓荒 (消耗 40 PP)")
            st.caption("隨機吞併 1~5 格中立灰色荒漠。在中原瘋狂擴張的同時，有 35% 機率隨機引爆邊境摩擦，導致隨機大國對你的仇恨度飆升！")
            
            if st.button("發動集團軍拓荒！", use_container_width=True):
                if player_stats["pp"] >= 40:
                    player_stats["pp"] -= 40
                    neutral_coords = [(r, c) for r in range(MAP_SIZE) for c in range(MAP_SIZE) if st.session_state.grid_map[r][c] == "中立荒漠"]
                    if neutral_coords:
                        conquest_count = min(len(neutral_coords), np.random.randint(1, 6))
                        chosen_spots = [neutral_coords[i] for i in np.random.choice(len(neutral_coords), conquest_count, replace=False)]
                        temp_arr = np.array(st.session_state.grid_map)
                        for r, c in chosen_spots: temp_arr[r, c] = current_player
                        st.session_state.grid_map = temp_arr.tolist()
                        st.session_state.battle_log.insert(0, f"⚡ 拓荒：【{current_user_name}({current_player})】擴張吞併了 {conquest_count} 格中立區！(產線基礎規模擴大)")
                        
                        if np.random.rand() < 0.35:
                            active_enemies = [c for c in COUNTRIES if c != current_player and c not in st.session_state.dead_players]
                            if active_enemies:
                                hit_country = np.random.choice(active_enemies)
                                clash_gain = np.random.randint(10, 21)
                                player_stats["animosity"][hit_country] = min(100, player_stats["animosity"][hit_country] + clash_gain)
                                st.session_state.player_data[hit_country]["animosity"][current_player] = min(100, st.session_state.player_data[hit_country]["animosity"][current_player] + clash_gain)
                                st.session_state.battle_log.insert(0, f"💥 邊境擦槍走火！我軍在開拓邊疆時與【{hit_country}】守軍發生零星摩擦，雙方仇恨飆升 {clash_gain} 點！")
                        st.rerun()
                    else: st.error("❌ 全地圖中立荒漠已被瓜分完畢！請改用選項一精準突擊對手領土！")
                player_stats["stockpile"]["火砲"] += player_stats["allocation"]["火砲"] * 80
            if player_stats["tech"]["中型戰車"] == "✅ 已解鎖": 
                player_stats["stockpile"]["戰車"] += player_stats["allocation"]["戰車"] * 15
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
                    for r, c in chunks[0]: temp_map[r, c] = "法西斯蘇聯" 
                if len(chunks) > 1:
                    for r, c in chunks[1]: temp_map[r, c] = "民主蘇聯"   
                if len(chunks) > 2:
                    for r, c in chunks[2]: temp_map[r, c] = "君主蘇聯"   
                if len(chunks) > 3:
                    for r, c in chunks[3]: temp_map[r, c] = "蘇維埃社會主義共和國聯邦（蘇聯）"
                st.session_state.grid_map = temp_map.tolist()
                
                sov_data = st.session_state.player_data["蘇維埃社會主義共和國聯邦（蘇聯）"]
                sov_data["base_civ"] = max(1, int(sov_data["base_civ"] * 0.25))
                sov_data["manpower"] = int(sov_data["manpower"] * 0.25)
                sov_data["stockpile"]["步槍"] = int(sov_data["stockpile"]["步槍"] * 0.25)
                sov_data["stockpile"]["火砲"] = int(sov_data["stockpile"]["火砲"] * 0.25)
                sov_data["stockpile"]["戰車"] = int(sov_data["stockpile"]["戰車"] * 0.25)
                st.session_state.soviet_collapsed = True
                st.session_state.battle_log.insert(0, f"🚨🚨 歷史震撼事件：蘇聯二次大內戰引爆！！最高蘇維埃政權瓦解，全境瞬間四分五裂！")
        st.rerun()

    if st.button("🔄 重新整場遊戲（返回選國）", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("📡 我國對各強權仇恨度")
    if current_player not in st.session_state.dead_players:
        for enemy, val in player_stats["animosity"].items():
            status = "⚔️ 可宣戰" if val >= 100 else "🕊️ 和平中"
            st.write(f"對【{enemy}】：`{val} / 100` ➔ **{status}**")
    else:
        st.write("🏳️ 國家已不存在，外交仇恨矩陣關閉。")

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
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='#1e1e1e')
    ax.set_facecolor('#111111')
    for row in range(MAP_SIZE):
        for col in range(MAP_SIZE):
            owner = st.session_state.grid_map[row][col]
            color = COLOR_MAP[owner]
            rect = plt.Rectangle((col, MAP_SIZE - 1 - row), 1, 1, linewidth=0.5, edgecolor='#222222', facecolor=color, alpha=0.9)
            ax.add_patch(rect)
            if owner != "中立荒漠":
                lbl = owner[:2]
                if owner == "德意志第三帝國（納粹德國）": lbl = "德意"
                elif owner == "蘇維埃社會主義共和國聯邦（蘇聯）": lbl = "蘇聯"
                elif owner == "中華蘇維埃反國抗日革命軍": lbl = "蘇抗"
                elif owner == "法西斯蘇聯": lbl = "白蘇"
                elif owner == "民主蘇聯": lbl = "黃蘇"
                elif owner == "君主蘇聯": lbl = "綠蘇"
                ax.text(col+0.5, MAP_SIZE - 1 - row + 0.5, lbl, color='black' if color in ['#ffffff', '#ffcc00'] else 'white', ha='center', va='center', fontsize=7, weight='bold')
    ax.set_xlim(0, MAP_SIZE)
    ax.set_ylim(0, MAP_SIZE)
    st.pyplot(fig)
    plt.close(fig)
    
    st.subheader("📊 全球版圖控制統計")
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("🔵 中華民國" + (" (已亡國)" if "中華民國" in st.session_state.dead_players else ""), f"{counts_current['中華民國']} 格")
    mc2.metric("⚫ 德意志第三帝國" + (" (已亡國)" if "德意志第三帝國（納粹德國）" in st.session_state.dead_players else ""), f"{counts_current['德意志第三帝國（納粹德國）']} 格")
    mc3.metric("💗 大日本帝國" + (" (已亡國)" if "大日本帝國" in st.session_state.dead_players else ""), f"{counts_current['大日本帝國']} 格")
    mc4.metric("🔴 蘇維埃聯邦" + (" (已亡國)" if "蘇維埃社會主義共和國聯邦（蘇聯）" in st.session_state.dead_players else ""), f"{counts_current['蘇維埃社會主義共和國聯邦（蘇聯）']} 格")
    
    st.markdown("---")
    st.metric("🥮 中華蘇維埃反國抗日革命軍（核心根據地）", f"{counts_current['中華蘇維埃反國抗日革命軍']} 格")

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
            st.markdown("##### 🚜 中型戰車 (1941)")
            tank_status = player_stats["tech"]["中型戰車"]
            if tank_status == "🔒 未研發" and player_stats["pp"] >= 150:
                if st.button("🧪 消耗 150 PP 研發裝甲裝備", key="t_tech"):
                    player_stats["pp"] -= 150
                    player_stats["tech"]["中型戰車"] = "✅ 已解鎖"
                    st.rerun()
            else: st.write(f"當前狀態: **{tank_status}**")

        st.markdown("---")
        st.subheader("🏭 本輪軍用工廠產線分配")
        current_max_mil = player_stats['mil_factories']
        
        if player_stats['allocation']['步槍'] + player_stats['allocation']['火砲'] + player_stats['allocation']['戰車'] > current_max_mil:
            player_stats['allocation']['步槍'] = current_max_mil
            player_stats['allocation']['火砲'] = 0
            player_stats['allocation']['戰車'] = 0

        safe_alloc_rifle = min(player_stats['allocation']['步槍'], current_max_mil)
        alloc_rifle = st.number_input("分配給【步槍產線】的工廠數", 0, current_max_mil, safe_alloc_rifle, key=f"ar_{current_player}")
        remaining_after_rifle = max(0, current_max_mil - alloc_rifle)
        safe_alloc_art = min(player_stats['allocation']['火砲'], remaining_after_rifle)
        alloc_art = st.number_input("分配給【火砲產線】的工廠數", 0, remaining_after_rifle, safe_alloc_art, key=f"aa_{current_player}")
        remaining_after_art = max(0, remaining_after_rifle - alloc_art)
        safe_alloc_tank = min(player_stats['allocation']['戰車'], remaining_after_art)
        alloc_tank = st.number_input("分配給【戰車產線】的工廠數", 0, remaining_after_art, safe_alloc_tank, key=f"at_{current_player}")
        
        if st.button("⚙️ 儲存本輪產線配置", use_container_width=True, key=f"save_mil_{current_player}"):
            player_stats['allocation']['步槍'] = alloc_rifle
            player_stats['allocation']['火砲'] = alloc_art
            player_stats['allocation']['戰車'] = alloc_tank
            st.success("⚙️ 軍工生產線配置成功更新！")
            st.rerun()
