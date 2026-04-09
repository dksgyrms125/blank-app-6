import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="확률 몬스터 드롭 실험", page_icon="🎯", layout="centered")

st.title("🎯 확률 학습: 클릭 몬스터 드롭 실험")
st.caption("몬스터를 클릭해서 처치하고, 아이템 드롭 확률이 실제로 어떻게 수렴하는지 확인해 보세요.")

st.markdown(
        """
### 실험 규칙
- 몬스터를 클릭하면 1회 처치로 기록됩니다.
- 처치마다 아이템이 1개 드롭됩니다.

처치 횟수가 많아질수록 아이템 비율이 어떻게 변하는지 관찰해 보세요.
"""
)

components.html(
        """
        <style>
            :root {
                --bg1: #1b2735;
                --bg2: #2f4f4f;
                --card: rgba(255, 255, 255, 0.08);
                --line: rgba(255, 255, 255, 0.2);
                --text: #f4f7fb;
                --muted: #c9d3df;
                --legendary: #ffd166;
                --rare: #72ddf7;
                --common: #b8f2e6;
            }

            * { box-sizing: border-box; }

            body {
                margin: 0;
                font-family: "Trebuchet MS", "Segoe UI", sans-serif;
                color: var(--text);
                background:
                    radial-gradient(circle at 10% 0%, #3a6073 0%, transparent 35%),
                    radial-gradient(circle at 90% 100%, #16222a 0%, transparent 30%),
                    linear-gradient(145deg, var(--bg1), var(--bg2));
            }

            .arena {
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 18px;
                backdrop-filter: blur(2px);
            }

            .top {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                margin-bottom: 12px;
            }

            .top h3 {
                margin: 0;
                font-size: 1.05rem;
            }

            .kills {
                font-weight: 700;
                color: #ffffff;
                background: rgba(0, 0, 0, 0.22);
                border: 1px solid var(--line);
                padding: 6px 10px;
                border-radius: 999px;
            }

            .monster-zone {
                min-height: 220px;
                display: grid;
                place-items: center;
                background: rgba(0, 0, 0, 0.18);
                border: 1px dashed rgba(255, 255, 255, 0.18);
                border-radius: 14px;
                margin-bottom: 12px;
                overflow: hidden;
            }

            #monsterBtn {
                border: none;
                background: transparent;
                cursor: pointer;
                padding: 0;
                transition: transform 0.12s ease;
            }

            #monsterBtn:hover { transform: translateY(-2px) scale(1.02); }
            #monsterBtn:active { transform: scale(0.96); }

            #monster {
                width: 170px;
                filter: drop-shadow(0 12px 16px rgba(0, 0, 0, 0.35));
                transform-origin: center bottom;
            }

            .hit #monster {
                animation: hitShake 0.22s ease;
            }

            .dead #monster {
                animation: defeat 0.55s ease forwards;
            }

            @keyframes hitShake {
                0% { transform: translateX(0); }
                25% { transform: translateX(-8px); }
                50% { transform: translateX(8px); }
                75% { transform: translateX(-5px); }
                100% { transform: translateX(0); }
            }

            @keyframes defeat {
                0% { transform: translateY(0) rotate(0) scale(1); opacity: 1; }
                50% { transform: translateY(-12px) rotate(-8deg) scale(1.08); opacity: 1; }
                100% { transform: translateY(70px) rotate(18deg) scale(0.25); opacity: 0; }
            }

            .drop-msg {
                min-height: 26px;
                text-align: center;
                font-weight: 700;
                margin-bottom: 10px;
            }

            .actions {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 12px;
            }

            #bulkKillBtn,
            #resetBtn {
                border: 1px solid rgba(255, 255, 255, 0.28);
                background: rgba(255, 255, 255, 0.12);
                color: var(--text);
                border-radius: 999px;
                padding: 8px 14px;
                font-weight: 700;
                cursor: pointer;
                transition: transform 0.12s ease, opacity 0.12s ease;
            }

            #bulkKillBtn:disabled,
            #resetBtn:disabled {
                opacity: 0.45;
                cursor: not-allowed;
            }

            #bulkKillBtn:not(:disabled):hover,
            #resetBtn:not(:disabled):hover {
                transform: translateY(-1px);
            }

            #resetBtn {
                background: rgba(255, 130, 130, 0.18);
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 8px;
            }

            .card {
                background: var(--card);
                border: 1px solid var(--line);
                border-radius: 12px;
                padding: 10px;
            }

            .label {
                font-size: 0.82rem;
                color: var(--muted);
            }

            .value {
                margin-top: 5px;
                font-size: 0.98rem;
                font-weight: 700;
            }

            .legendary { color: var(--legendary); }
            .rare { color: var(--rare); }
            .common { color: var(--common); }

            .probability-panel {
                margin-top: 10px;
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid var(--line);
                border-radius: 12px;
                padding: 10px;
            }

            .probability-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 8px;
            }

            .prob-item label {
                display: block;
                font-size: 0.8rem;
                color: var(--muted);
                margin-bottom: 4px;
            }

            .prob-item input {
                width: 100%;
                border: 1px solid rgba(255, 255, 255, 0.24);
                background: rgba(255, 255, 255, 0.08);
                color: var(--text);
                border-radius: 8px;
                padding: 7px 8px;
                font-weight: 700;
            }

            .prob-status {
                margin-top: 8px;
                text-align: center;
                font-size: 0.82rem;
                color: var(--muted);
                min-height: 20px;
            }

            .prob-status.error {
                color: #ffb3b3;
            }

            .prob-status.success {
                color: #b8f2e6;
            }

            #checkAnswerBtn {
                margin-top: 8px;
                width: 100%;
                border: 1px solid rgba(255, 255, 255, 0.28);
                background: rgba(114, 221, 247, 0.2);
                color: var(--text);
                border-radius: 10px;
                padding: 8px 12px;
                font-weight: 700;
                cursor: pointer;
            }

            .footer {
                margin-top: 10px;
                font-size: 0.82rem;
                color: var(--muted);
                text-align: center;
            }

            @media (max-width: 640px) {
                .cards { grid-template-columns: 1fr; }
                #monster { width: 145px; }
            }
        </style>

        <div class="arena" id="arena">
            <div class="top">
                <h3>몬스터 사냥</h3>
                <div class="kills" id="killCounter">처치 수: 0</div>
            </div>

            <div class="monster-zone" id="monsterZone">
                <button id="monsterBtn" aria-label="몬스터 공격">
                    <svg id="monster" viewBox="0 0 220 220" role="img" aria-label="슬라임 몬스터">
                        <defs>
                            <radialGradient id="bodyGrad" cx="30%" cy="25%" r="70%">
                                <stop offset="0%" stop-color="#9bf6ff" />
                                <stop offset="100%" stop-color="#1f7a8c" />
                            </radialGradient>
                        </defs>
                        <ellipse cx="110" cy="182" rx="58" ry="16" fill="rgba(0,0,0,0.2)"/>
                        <path d="M42 130 C42 66, 78 30, 110 30 C142 30, 178 66, 178 130 C178 166, 147 190, 110 190 C73 190, 42 166, 42 130 Z"
                                    fill="url(#bodyGrad)" stroke="#dff9ff" stroke-width="4"/>
                        <circle cx="83" cy="115" r="16" fill="#ffffff"/>
                        <circle cx="137" cy="115" r="16" fill="#ffffff"/>
                        <circle cx="87" cy="119" r="6" fill="#143642"/>
                        <circle cx="141" cy="119" r="6" fill="#143642"/>
                        <path d="M83 152 Q110 170 137 152" fill="none" stroke="#143642" stroke-width="6" stroke-linecap="round"/>
                        <circle cx="70" cy="74" r="8" fill="#b8fff9" opacity="0.7"/>
                    </svg>
                </button>
            </div>

            <div class="drop-msg" id="dropMsg">몬스터를 클릭해 시작하세요!</div>

            <div class="actions">
                <button id="bulkKillBtn" disabled>10마리 연속 처치 (31마리부터)</button>
                <button id="resetBtn">초기화</button>
            </div>

            <div class="cards">
                <div class="card">
                    <div class="label">전설 아이템</div>
                    <div class="value legendary" id="legendaryStat">0개</div>
                </div>
                <div class="card">
                    <div class="label">희귀 아이템</div>
                    <div class="value rare" id="rareStat">0개</div>
                </div>
                <div class="card">
                    <div class="label">일반 아이템</div>
                    <div class="value common" id="commonStat">0개</div>
                </div>
            </div>

            <div class="probability-panel">
                <div class="label">이론 확률 추론 퀴즈 (%): 표본확률을 보고 값을 추측해 보세요.</div>
                <div class="probability-grid">
                    <div class="prob-item">
                        <label for="legendaryRate">전설</label>
                        <input id="legendaryRate" type="number" min="0" max="100" step="0.1" />
                    </div>
                    <div class="prob-item">
                        <label for="rareRate">희귀</label>
                        <input id="rareRate" type="number" min="0" max="100" step="0.1" />
                    </div>
                    <div class="prob-item">
                        <label for="commonRate">일반</label>
                        <input id="commonRate" type="number" min="0" max="100" step="0.1" />
                    </div>
                </div>
                <button id="checkAnswerBtn">정답 확인</button>
                <div class="prob-status" id="probStatus">세 값을 입력하고 정답 확인을 눌러보세요.</div>
            </div>

            <div class="footer">팁: 표본이 커질수록 비율 변화가 더 안정적으로 보입니다.</div>
        </div>

        <script>
            const arena = document.getElementById("arena");
            const monsterBtn = document.getElementById("monsterBtn");
            const killCounter = document.getElementById("killCounter");
            const dropMsg = document.getElementById("dropMsg");
            const bulkKillBtn = document.getElementById("bulkKillBtn");
            const resetBtn = document.getElementById("resetBtn");
            const legendaryStat = document.getElementById("legendaryStat");
            const rareStat = document.getElementById("rareStat");
            const commonStat = document.getElementById("commonStat");
            const legendaryRateInput = document.getElementById("legendaryRate");
            const rareRateInput = document.getElementById("rareRate");
            const commonRateInput = document.getElementById("commonRate");
            const checkAnswerBtn = document.getElementById("checkAnswerBtn");
            const probStatus = document.getElementById("probStatus");

            const trueRates = {
                legendary: 5,
                rare: 25,
                common: 70,
            };

            const state = {
                kills: 0,
                legendary: 0,
                rare: 0,
                common: 0,
                locked: false,
            };

            function pct(count) {
                if (state.kills === 0) return "0.00";
                return ((count / state.kills) * 100).toFixed(2);
            }

            function formatStat(count) {
                if (state.kills >= 50) {
                    return `${count}개 · ${pct(count)}%`;
                }
                return `${count}개`;
            }

            function updateUI() {
                killCounter.textContent = `처치 수: ${state.kills}`;
                legendaryStat.textContent = formatStat(state.legendary);
                rareStat.textContent = formatStat(state.rare);
                commonStat.textContent = formatStat(state.common);
                bulkKillBtn.disabled = state.kills <= 30 || state.locked;
                monsterBtn.disabled = state.locked;
                resetBtn.disabled = state.locked;
            }

            function nearlyEqual(a, b) {
                return Math.abs(a - b) < 0.0001;
            }

            function checkAnswer() {
                const guessedLegendary = Number(legendaryRateInput.value);
                const guessedRare = Number(rareRateInput.value);
                const guessedCommon = Number(commonRateInput.value);

                if (!Number.isFinite(guessedLegendary) || !Number.isFinite(guessedRare) || !Number.isFinite(guessedCommon)) {
                    probStatus.classList.remove("success");
                    probStatus.classList.add("error");
                    probStatus.textContent = "세 칸 모두 숫자를 입력해 주세요.";
                    return;
                }

                const isCorrect =
                    nearlyEqual(guessedLegendary, trueRates.legendary) &&
                    nearlyEqual(guessedRare, trueRates.rare) &&
                    nearlyEqual(guessedCommon, trueRates.common);

                if (isCorrect) {
                    probStatus.classList.remove("error");
                    probStatus.classList.add("success");
                    probStatus.textContent = "정답입니다! (전설 5%, 희귀 25%, 일반 70%)";
                } else {
                    probStatus.classList.remove("success");
                    probStatus.classList.add("error");
                    probStatus.textContent = "오답입니다. 표본확률을 더 관찰하고 다시 추측해 보세요.";
                }
            }

            function rollDrop() {
                const r = Math.random() * 100;
                if (r < trueRates.legendary) return "legendary";
                if (r < trueRates.legendary + trueRates.rare) return "rare";
                return "common";
            }

            function messageFor(item) {
                if (item === "legendary") return "✨ 전설 아이템 드롭!";
                if (item === "rare") return "🔹 희귀 아이템 획득!";
                return "⚪ 일반 아이템 획득!";
            }

            function addDrop(item) {
                state.kills += 1;
                state[item] += 1;
            }

            function resetAll() {
                state.kills = 0;
                state.legendary = 0;
                state.rare = 0;
                state.common = 0;
                dropMsg.textContent = "기록이 초기화되었습니다. 다시 시작하세요!";
                updateUI();
            }

            monsterBtn.addEventListener("click", () => {
                if (state.locked) return;
                state.locked = true;

                arena.classList.remove("hit", "dead");
                void arena.offsetWidth;
                arena.classList.add("hit");

                const dropped = rollDrop();
                addDrop(dropped);
                dropMsg.textContent = messageFor(dropped);
                updateUI();

                setTimeout(() => {
                    arena.classList.add("dead");
                }, 120);

                setTimeout(() => {
                    arena.classList.remove("hit", "dead");
                    state.locked = false;
                    updateUI();
                }, 620);
            });

            bulkKillBtn.addEventListener("click", () => {
                if (state.locked || state.kills <= 30) return;
                state.locked = true;
                updateUI();

                arena.classList.remove("hit", "dead");
                void arena.offsetWidth;
                arena.classList.add("hit");

                const batch = { legendary: 0, rare: 0, common: 0 };
                for (let i = 0; i < 10; i += 1) {
                    const dropped = rollDrop();
                    addDrop(dropped);
                    batch[dropped] += 1;
                }

                dropMsg.textContent = `⚔️ 10마리 처치 완료! 전설 ${batch.legendary} · 희귀 ${batch.rare} · 일반 ${batch.common}`;
                updateUI();

                setTimeout(() => {
                    arena.classList.add("dead");
                }, 100);

                setTimeout(() => {
                    arena.classList.remove("hit", "dead");
                    state.locked = false;
                    updateUI();
                }, 560);
            });

            resetBtn.addEventListener("click", () => {
                if (state.locked) return;
                resetAll();
            });

            checkAnswerBtn.addEventListener("click", checkAnswer);

            updateUI();
        </script>
        """,
        height=700,
)
