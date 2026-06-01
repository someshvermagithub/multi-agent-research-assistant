import streamlit as st
import time
import json
from datetime import datetime
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Mind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e6f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e2e;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #9b97b0 !important;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: #6b6880;
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.05em;
}

/* Input area */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #13131f !important;
    border: 1px solid #2a2840 !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.15) !important;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(124,58,237,0.5) !important;
}

/* Cards */
.card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.8rem;
}
.card-badge {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
}
.badge-search  { background:#1e1030; color:#c084fc; border:1px solid #3d1f5e; }
.badge-reader  { background:#0f1e30; color:#38bdf8; border:1px solid #1a3f5e; }
.badge-writer  { background:#0f2018; color:#4ade80; border:1px solid #1a4530; }
.badge-critic  { background:#1e1510; color:#fb923c; border:1px solid #4a2e10; }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #c8c4e0;
}
.card-body {
    color: #9b97b0;
    font-size: 0.88rem;
    line-height: 1.65;
    white-space: pre-wrap;
}

/* Step tracker */
.step-tracker {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin: 1.2rem 0;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #2a2840;
    transition: all 0.3s;
}
.step-dot.active  { background: #818cf8; box-shadow: 0 0 8px #818cf8; }
.step-dot.done    { background: #4ade80; }
.step-line {
    flex: 1; height: 1px;
    background: #2a2840;
}

/* Score display */
.score-ring {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fb923c, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* History item */
.history-item {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color 0.2s;
}
.history-item:hover { border-color: #3d3a5e; }
.history-topic {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #c8c4e0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.history-time {
    font-size: 0.7rem;
    color: #4a4760;
    margin-top: 0.15rem;
}

/* Metric cards */
.metric-card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #818cf8;
}
.metric-label {
    font-size: 0.72rem;
    color: #4a4760;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Scrollable output */
.output-scroll {
    max-height: 340px;
    overflow-y: auto;
    padding-right: 0.3rem;
}
.output-scroll::-webkit-scrollbar { width: 4px; }
.output-scroll::-webkit-scrollbar-track { background: transparent; }
.output-scroll::-webkit-scrollbar-thumb { background: #2a2840; border-radius: 2px; }

/* Selectbox */
.stSelectbox > div > div {
    background: #13131f !important;
    border-color: #2a2840 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}

/* Divider */
hr { border-color: #1e1e2e !important; }

/* Spinner overlay text */
.stSpinner > div { border-top-color: #818cf8 !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #13131f !important;
    border-radius: 10px !important;
    color: #9b97b0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Download button */
[data-testid="baseButton-secondary"] {
    background: #13131f !important;
    border: 1px solid #2a2840 !important;
    color: #9b97b0 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []        # list of dicts
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "total_researches" not in st.session_state:
    st.session_state.total_researches = 0


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem'>
        <span style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;
                     background:linear-gradient(135deg,#c084fc,#818cf8);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                     background-clip:text;'>🧠 Research Mind</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Agent status panel ────
    st.markdown("<p style='color:#4a4760;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>Agent Pipeline</p>", unsafe_allow_html=True)

    agents = [
        ("🔍", "Search Agent",  "Tavily web search",      "#c084fc"),
        ("📖", "Reader Agent",  "URL scraper",            "#38bdf8"),
        ("✍️", "Writer Chain",  "Report drafting",        "#4ade80"),
        ("🔬", "Critic Chain",  "Quality scoring",        "#fb923c"),
    ]
    for icon, name, desc, color in agents:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:0.7rem;
                    padding:0.55rem 0.7rem;margin-bottom:0.4rem;
                    background:#0a0a0f;border-radius:8px;
                    border:1px solid #1e1e2e;'>
            <span style='font-size:1rem;'>{icon}</span>
            <div>
                <div style='font-family:Syne,sans-serif;font-size:0.78rem;
                            font-weight:700;color:{color};'>{name}</div>
                <div style='font-size:0.68rem;color:#4a4760;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Stats ─────────────────
    st.markdown("<p style='color:#4a4760;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>Session Stats</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{st.session_state.total_researches}</div>
            <div class='metric-label'>Reports</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(st.session_state.history)}</div>
            <div class='metric-label'>Saved</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── History ───────────────
    st.markdown("<p style='color:#4a4760;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;'>Research History</p>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("<p style='color:#2a2840;font-size:0.8rem;text-align:center;padding:1rem 0;'>No history yet</p>", unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history[-8:])):
            if st.button(f"📄 {item['topic'][:28]}…" if len(item['topic']) > 28 else f"📄 {item['topic']}", key=f"hist_{i}", use_container_width=True):
                st.session_state.current_result = item['result']
                st.session_state.loaded_topic = item['topic']


# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 2rem 0 1.5rem'>
    <div class='hero-title'>Research Mind</div>
    <div class='hero-sub'>Multi-agent AI research pipeline · Search → Read → Write → Critique</div>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="",
        placeholder="🔭  Enter any research topic…  e.g. 'Quantum computing in 2025'",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Research →", use_container_width=True)

# ── Quick topics ──────────────────────────────────────────────────────────────
st.markdown("<p style='color:#4a4760;font-size:0.72rem;margin:0.4rem 0 0.6rem;'>Quick topics →</p>", unsafe_allow_html=True)
quick = ["Artificial General Intelligence", "CRISPR gene editing 2025", "Climate tech innovations", "Neuralink progress"]
qcols = st.columns(len(quick))
chosen_quick = None
for i, q in enumerate(quick):
    with qcols[i]:
        if st.button(q, key=f"quick_{i}", use_container_width=True):
            chosen_quick = q

if chosen_quick:
    topic = chosen_quick

# ── Run pipeline ──────────────────────────────────────────────────────────────
if (run_btn or chosen_quick) and topic.strip():

    st.session_state.current_result = None   # clear old result
    progress_placeholder = st.empty()

    steps = [
        ("🔍", "Search Agent", "Searching the web for recent sources…",     "badge-search"),
        ("📖", "Reader Agent", "Scraping top URLs for deeper content…",      "badge-reader"),
        ("✍️", "Writer Chain", "Drafting a structured research report…",     "badge-writer"),
        ("🔬", "Critic Chain",  "Evaluating report quality and scoring…",    "badge-critic"),
    ]

    def render_progress(active_step):
        dots = "".join(
            f"<div class='step-dot {'active' if i == active_step else 'done' if i < active_step else ''}'></div>"
            + ("<div class='step-line'></div>" if i < len(steps)-1 else "")
            for i in range(len(steps))
        )
        icon, name, desc, badge = steps[active_step]
        progress_placeholder.markdown(f"""
        <div class='card' style='border-color:#2a2840;'>
            <div class='step-tracker'>{dots}</div>
            <div style='display:flex;align-items:center;gap:0.5rem;margin-top:0.5rem;'>
                <span style='font-size:1.3rem;'>{icon}</span>
                <div>
                    <span class='card-badge {badge}'>Step {active_step+1}/4</span>
                    <div style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
                                color:#c8c4e0;margin-top:0.2rem;'>{name}</div>
                    <div style='font-size:0.82rem;color:#6b6880;'>{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Monkey-patch pipeline steps to show live progress
    # We run the full pipeline but update progress at key moments
    import agents as ag_module
    import pipeline as pl_module

    original_run = pl_module.run_research_pipeline

    result_holder = {}

    with st.spinner(""):
        try:
            render_progress(0)
            time.sleep(0.4)

            # We can't easily hook into the pipeline mid-run in streamlit,
            # so we run it and update progress based on timing heuristics.
            # For a better DX we wrap and run with incremental status updates.

            import threading

            state_ref = {}
            error_ref = {}

            def run_in_thread():
                try:
                    state_ref["result"] = original_run(topic.strip())
                except Exception as e:
                    error_ref["error"] = str(e)

            t = threading.Thread(target=run_in_thread, daemon=True)
            t.start()

            # Show animated steps while waiting
            step_times = [0, 8, 18, 26]   # rough seconds per step
            step_idx = 0
            elapsed = 0
            while t.is_alive():
                if step_idx < 3 and elapsed >= step_times[step_idx + 1]:
                    step_idx += 1
                render_progress(step_idx)
                time.sleep(1)
                elapsed += 1

            t.join()
            render_progress(3)
            time.sleep(0.5)
            progress_placeholder.empty()

            if "error" in error_ref:
                st.error(f"Pipeline error: {error_ref['error']}")
            else:
                result = state_ref["result"]
                st.session_state.current_result = result
                st.session_state.total_researches += 1
                st.session_state.history.append({
                    "topic": topic.strip(),
                    "result": result,
                    "time": datetime.now().strftime("%H:%M · %d %b"),
                })
                st.session_state.loaded_topic = topic.strip()

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"Unexpected error: {e}")

# ── Display results ───────────────────────────────────────────────────────────
res = st.session_state.current_result
topic_label = getattr(st.session_state, "loaded_topic", "")

if res:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:0.8rem;margin:1.5rem 0 1rem;'>
        <div style='width:3px;height:2rem;background:linear-gradient(#c084fc,#818cf8);border-radius:2px;'></div>
        <div>
            <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#c8c4e0;'>
                {topic_label}
            </div>
            <div style='font-size:0.75rem;color:#4a4760;'>Research complete · {datetime.now().strftime("%d %b %Y, %H:%M")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Full Report", "🔍 Search Results", "🌐 Scraped Content", "🔬 Critic Review"])

    # ── Tab 1: Report ──────────────────────────────────────────────────────────
    with tab1:
        report_text = res.get("report", "No report generated.")
        if hasattr(report_text, "content"):
            report_text = report_text.content

        # Parse sections
        sections = {"intro": "", "findings": "", "conclusion": "", "sources": ""}
        current = "intro"
        lines = str(report_text).split("\n")
        for line in lines:
            ll = line.lower()
            if "key finding" in ll or "findings" in ll:
                current = "findings"
            elif "conclusion" in ll:
                current = "conclusion"
            elif "source" in ll or "reference" in ll:
                current = "sources"
            sections[current] += line + "\n"

        # Score from critic
        critic_raw = res.get("feedback", "")
        if hasattr(critic_raw, "content"):
            critic_raw = critic_raw.content
        critic_str = str(critic_raw)
        score_display = "–"
        for line in critic_str.split("\n"):
            if "score" in line.lower() and "/" in line:
                score_display = line.split(":")[-1].strip().split("/")[0].strip()
                break

        # Metrics row
        mc1, mc2, mc3, mc4 = st.columns(4)
        for col, val, label in [
            (mc1, score_display + "/10", "Critic Score"),
            (mc2, str(len(str(report_text).split())), "Words"),
            (mc3, str(len([l for l in lines if l.strip().startswith("-")])), "Key Points"),
            (mc4, str(str(report_text).count("http")), "Sources"),
        ]:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='font-size:1.3rem;'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        for label, badge, content in [
            ("Introduction", "badge-search", sections["intro"]),
            ("Key Findings", "badge-writer", sections["findings"]),
            ("Conclusion", "badge-critic", sections["conclusion"]),
            ("Sources", "badge-reader", sections["sources"]),
        ]:
            if content.strip():
                st.markdown(f"""
                <div class='card'>
                    <div class='card-header'>
                        <span class='card-badge {badge}'>{label}</span>
                    </div>
                    <div class='card-body output-scroll'>{content.strip()}</div>
                </div>""", unsafe_allow_html=True)

        # Download
        st.download_button(
            "⬇ Download Report (.txt)",
            data=str(report_text),
            file_name=f"research_{topic_label[:30].replace(' ','_')}.txt",
            mime="text/plain",
        )

    # ── Tab 2: Search Results ─────────────────────────────────────────────────
    with tab2:
        sr = res.get("search_results", "No search results.")
        if hasattr(sr, "content"):
            sr = sr.content
        entries = str(sr).split("----")
        for entry in entries:
            if entry.strip():
                lines_e = [l.strip() for l in entry.strip().split("\n") if l.strip()]
                title = next((l.replace("Title:", "").strip() for l in lines_e if l.startswith("Title:")), "Result")
                url   = next((l.replace("URL:", "").strip() for l in lines_e if l.startswith("URL:")), "")
                snip  = next((l.replace("Snippet:", "").strip() for l in lines_e if l.startswith("Snippet:")), "")
                st.markdown(f"""
                <div class='card'>
                    <div style='font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#c8c4e0;margin-bottom:0.3rem;'>
                        🔗 {title}
                    </div>
                    <div style='font-size:0.75rem;color:#818cf8;margin-bottom:0.5rem;word-break:break-all;'>{url}</div>
                    <div style='font-size:0.85rem;color:#9b97b0;line-height:1.6;'>{snip}</div>
                </div>""", unsafe_allow_html=True)

    # ── Tab 3: Scraped Content ────────────────────────────────────────────────
    with tab3:
        sc = res.get("scraped_content", "No scraped content.")
        if hasattr(sc, "content"):
            sc = sc.content
        st.markdown(f"""
        <div class='card'>
            <div class='card-header'>
                <span class='card-badge badge-reader'>Scraped Content</span>
                <span class='card-title'>Raw extracted text from top source</span>
            </div>
            <div class='card-body output-scroll'>{str(sc)}</div>
        </div>""", unsafe_allow_html=True)

    # ── Tab 4: Critic Review ──────────────────────────────────────────────────
    with tab4:
        fb = res.get("feedback", "No feedback generated.")
        if hasattr(fb, "content"):
            fb = fb.content
        fb_str = str(fb)

        # Parse structured feedback
        parsed = {"score": "–", "strengths": [], "improve": [], "verdict": ""}
        for line in fb_str.split("\n"):
            ls = line.strip()
            if ls.lower().startswith("score:"):
                parsed["score"] = ls.split(":", 1)[-1].strip()
            elif ls.startswith("- ") and "Strengths" not in fb_str[:fb_str.find(ls)].split("\n")[-3:]:
                parsed["improve"].append(ls[2:])
            elif ls.startswith("- "):
                parsed["strengths"].append(ls[2:])
            elif "verdict" in ls.lower() and ":" in ls:
                parsed["verdict"] = ls.split(":", 1)[-1].strip()

        # Score display
        raw_score = parsed["score"].replace("/10", "").strip()
        try:
            score_num = float(raw_score)
            score_color = "#4ade80" if score_num >= 7 else "#fb923c" if score_num >= 5 else "#f87171"
        except:
            score_color = "#818cf8"

        st.markdown(f"""
        <div style='text-align:center;padding:2rem 0 1rem;'>
            <div style='font-family:Syne,sans-serif;font-size:3.5rem;font-weight:800;
                        color:{score_color};line-height:1;'>{parsed["score"]}</div>
            <div style='font-size:0.8rem;color:#4a4760;text-transform:uppercase;
                        letter-spacing:0.1em;margin-top:0.4rem;'>Critic Score</div>
        </div>""", unsafe_allow_html=True)

        if parsed["verdict"]:
            st.markdown(f"""
            <div class='card' style='text-align:center;border-color:#2a2840;'>
                <div style='font-style:italic;font-size:0.95rem;color:#9b97b0;'>"{parsed["verdict"]}"</div>
            </div>""", unsafe_allow_html=True)

        col_s, col_i = st.columns(2)
        with col_s:
            st.markdown("""
            <div class='card'>
                <div class='card-header'>
                    <span class='card-badge badge-writer'>Strengths</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='card-body'>{fb_str}</div></div>", unsafe_allow_html=True)

        with col_i:
            st.markdown(f"""
            <div class='card'>
                <div class='card-header'>
                    <span class='card-badge badge-critic'>Full Review</span>
                </div>
                <div class='card-body output-scroll'>{fb_str}</div>
            </div>""", unsafe_allow_html=True)

elif not topic.strip() and not res:
    # Empty state
    st.markdown("""
    <div style='text-align:center;padding:4rem 2rem;'>
        <div style='font-size:3.5rem;margin-bottom:1rem;'>🧠</div>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;
                    color:#2a2840;margin-bottom:0.5rem;'>Ready to research</div>
        <div style='font-size:0.85rem;color:#2a2840;'>
            Enter a topic above and let the multi-agent pipeline<br>
            search, read, write and critique for you.
        </div>
    </div>
    """, unsafe_allow_html=True)