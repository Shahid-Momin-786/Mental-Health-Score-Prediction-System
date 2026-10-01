"""
app.py  |  Student Mental Health Score Predictor
Part 3 – Streamlit Deployment
"""

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(
    page_title="Student Mental Health Score Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def load_model():
    return joblib.load("Mental_Health_Model.pkl")

model = load_model()

TOP_COUNTRIES = ['India', 'USA', 'Canada', 'Australia', 'UK',
                 'Germany', 'Mexico', 'Turkey', 'France']

def score_category(s):
    if s >= 8.0: return "Excellent",  "#00d4aa", "🌟"
    if s >= 6.5: return "Good",       "#4ade80", "😊"
    if s >= 5.0: return "Moderate",   "#facc15", "😐"
    if s >= 3.5: return "Low",        "#fb923c", "😟"
    return              "Poor",       "#f87171", "😔"


# ─────────────────────────── GLOBAL CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Inter', sans-serif !important;
    background: #07071c !important;
    color: #e2e8f0 !important;
}
[data-testid="stMain"] { background: transparent !important; }
.block-container { padding: 1.2rem 1.8rem 2rem !important; max-width: 100% !important; }
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"] { display: none !important; }

/* animated gradient bg */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: -1;
    background:
        radial-gradient(ellipse 60% 55% at 12% 12%, rgba(109,40,217,0.30) 0%, transparent 60%),
        radial-gradient(ellipse 50% 45% at 88% 82%, rgba(5,150,105,0.20) 0%, transparent 55%),
        radial-gradient(ellipse 35% 30% at 65% 18%, rgba(190,24,93,0.10) 0%, transparent 50%),
        #07071c;
    animation: bgShift 16s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0%   { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(18deg) brightness(1.07); }
}

/* top nav */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.85rem 1.4rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(14px);
}
.brand { display:flex; align-items:center; gap:10px; }
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem; font-weight: 700; color: #fff;
}
.brand-name span { color: #a78bfa; }
.live-badge {
    display:flex; align-items:center; gap:6px;
    background: rgba(124,58,237,0.14);
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 100px; padding: 4px 13px;
    font-size: 0.73rem; font-weight: 600; color: #a78bfa;
    letter-spacing: 1px; text-transform: uppercase;
    animation: livePulse 3s ease-in-out infinite;
}
.live-dot { width:7px;height:7px;border-radius:50%;background:#a78bfa;
            animation: blink 1.8s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.25;} }
@keyframes livePulse { 0%,100%{box-shadow:0 0 0 transparent;}
                       50%{box-shadow:0 0 14px rgba(124,58,237,0.45);} }

/* left form panel */
.form-panel {
    background: rgba(12,12,32,0.78);
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 20px;
    padding: 1.5rem 1.3rem 1.3rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.45);
}
.panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem; font-weight: 700; color: #fff;
    margin-bottom: 1rem;
    display:flex; align-items:center; gap:8px;
}
.form-section {
    font-size: 0.66rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: #7c3aed;
    padding: 9px 0 4px;
    border-top: 1px solid rgba(124,58,237,0.18);
    margin-top: 6px; margin-bottom: 3px;
}

/* widget overrides */
label, .stSelectbox label, .stSlider label,
.stNumberInput label, .stTextInput label {
    font-size: 0.79rem !important; font-weight: 500 !important;
    color: #94a3b8 !important;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg,#7c3aed,#a78bfa) !important;
    border: 2px solid #c4b5fd !important;
    box-shadow: 0 0 10px rgba(124,58,237,0.55) !important;
}
.stSlider [data-baseweb="slider"] div[role="progressbar"] {
    background: linear-gradient(90deg,#7c3aed,#a78bfa) !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(124,58,237,0.28) !important;
    border-radius: 9px !important; color: #e2e8f0 !important;
}
.stSelectbox svg { fill:#7c3aed !important; }

/* predict button */
.stButton > button {
    width:100% !important;
    background: linear-gradient(135deg,#7c3aed,#5b21b6) !important;
    border:none !important; border-radius:12px !important;
    color:#fff !important;
    font-family:'Space Grotesk',sans-serif !important;
    font-weight:700 !important; font-size:1rem !important;
    padding:0.78rem !important; letter-spacing:0.3px !important;
    transition:all 0.25s !important;
    box-shadow:0 4px 22px rgba(124,58,237,0.45),
               inset 0 1px 0 rgba(255,255,255,0.12) !important;
    margin-top:6px !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 30px rgba(124,58,237,0.65) !important;
}

/* right panel cards */
.rpanel {
    background: rgba(12,12,32,0.78);
    border: 1px solid rgba(124,58,237,0.20);
    border-radius: 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.40);
    padding: 1.5rem 1.4rem 1.3rem;
}
.sdiv {
    font-size:0.66rem; font-weight:700; letter-spacing:2.5px;
    text-transform:uppercase; color:#7c3aed;
    display:flex; align-items:center; gap:8px;
    margin: 1rem 0 0.55rem;
}
.sdiv::after { content:''; flex:1; height:1px; background:rgba(124,58,237,0.2); }

/* metric tiles */
.metric-row { display:grid; grid-template-columns:repeat(3,1fr); gap:9px; margin-top:1rem; }
.metric-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 11px; padding:0.75rem 0.4rem;
    text-align:center; transition:all 0.2s;
}
.metric-box:hover {
    background:rgba(124,58,237,0.09);
    border-color:rgba(124,58,237,0.35);
    transform:translateY(-2px);
}
.m-icon { font-size:1.15rem; }
.m-val  { font-size:1.2rem; font-weight:700; margin:2px 0 1px; }
.m-lbl  { font-size:0.67rem; color:#475569; text-transform:uppercase; letter-spacing:0.8px; }

/* tip cards */
.tip-card {
    display:flex; gap:10px; align-items:flex-start;
    background:rgba(255,255,255,0.025);
    border:1px solid rgba(255,255,255,0.06);
    border-radius:11px; padding:0.8rem;
    margin-bottom:7px;
    transition:all 0.2s;
    animation: tipIn 0.4s ease both;
}
.tip-card:hover { border-color:rgba(124,58,237,0.3); background:rgba(124,58,237,0.06); }
@keyframes tipIn { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }
.t-em  { font-size:1.25rem; flex-shrink:0; margin-top:2px; }
.t-h   { font-weight:600; font-size:0.85rem; color:#e2e8f0; margin-bottom:2px; }
.t-p   { font-size:0.77rem; color:#64748b; line-height:1.55; }

/* bar chart */
.bar-row { display:flex; align-items:center; gap:8px; margin-bottom:6px; }
.bl { font-size:0.73rem; color:#64748b; width:82px; flex-shrink:0; }
.bb { flex:1; background:rgba(255,255,255,0.05); border-radius:100px; height:5px; overflow:hidden; }
.bf { height:100%; border-radius:100px; }
.bp { font-size:0.7rem; color:#7c3aed; width:28px; text-align:right; font-weight:600; }

/* score guide */
.gr {
    display:flex; justify-content:space-between; align-items:center;
    padding:5px 8px; border-radius:8px;
    background:rgba(255,255,255,0.02); margin-bottom:3px;
}

/* idle dashed box */
.idle-box {
    border: 2px dashed rgba(124,58,237,0.22);
    border-radius: 18px; padding: 2.5rem 2rem;
    text-align:center; margin-bottom: 1rem;
}

::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-thumb { background:rgba(124,58,237,0.4); border-radius:10px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── TOP NAV ──────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="brand">
    <span style="font-size:1.55rem;">🧠</span>
    <div class="brand-name">Mind<span>Score</span></div>
  </div>
  <div class="live-badge"><div class="live-dot"></div>ML Model Live</div>
  <div style="font-size:0.77rem;color:#475569;">
    Random Forest &nbsp;•&nbsp; R² = 0.83 &nbsp;•&nbsp; Part 3 Submission
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── LAYOUT ───────────────────────────────────────────
left, right = st.columns([1, 1.4], gap="large")

# ════════════════════ LEFT — FORM ════════════════════
with left:
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📋 Student Profile</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">👤 Personal Information</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: age    = st.slider("Age", 10, 50, 20)
    with c2: gender = st.selectbox("Gender", ["Male","Female"])
    c3, c4 = st.columns(2)
    with c3: country_input  = st.text_input("Country", "India")
    with c4: academic_level = st.selectbox("Academic Level",
                                ["Undergraduate","Graduate","High School"])

    st.markdown('<div class="form-section">📱 Social Media</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5: most_used_platform = st.selectbox("Platform",
                ["Instagram","YouTube","TikTok","Facebook","LinkedIn",
                 "Snapchat","Twitter","WhatsApp","WeChat","LINE","KakaoTalk","VKontakte"])
    with c6: purpose_of_use = st.selectbox("Purpose",
                ["Entertainment","Education","Networking","News"])
    avg_daily_usage_hours = st.slider("Daily Usage (hours)", 0.0, 12.0, 3.0, 0.5)
    daily_unlocks = st.number_input("Daily Phone Unlocks", 0, 300, 50, 5)

    st.markdown('<div class="form-section">🏃 Lifestyle & Wellbeing</div>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7: study_hours            = st.slider("Study Hours/Day",  0.0, 16.0, 5.0, 0.5)
    with c8: physical_activity_hours = st.slider("Activity (hrs)",  0.0,  8.0, 1.0, 0.25)
    c9, c10 = st.columns(2)
    with c9:  sleep_hours  = st.slider("Sleep Hours/Night", 0.0, 12.0, 7.0, 0.25)
    with c10: stress_level = st.selectbox("Stress Level", ["Low","Medium","High","Very High"])

    st.markdown("<br/>", unsafe_allow_html=True)
    predict_btn = st.button("⚡  Predict My Mental Health Score")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════ RIGHT — RESULTS ════════════════════
with right:
    if not predict_btn:
        # ── idle ──
        st.markdown("""
        <div class="idle-box">
          <div style="font-size:3.5rem;opacity:0.5;margin-bottom:0.8rem;">🎯</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;
                      font-weight:700;color:#6d28d9;margin-bottom:6px;">
            Your Score Appears Here
          </div>
          <div style="font-size:0.85rem;color:#475569;line-height:1.7;">
            Fill in the profile on the left and click<br/>
            <strong style="color:#a78bfa;">⚡ Predict</strong> to see your result.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # model facts
        st.markdown('<div class="rpanel">', unsafe_allow_html=True)
        st.markdown('<div class="sdiv">About the Model</div>', unsafe_allow_html=True)
        facts = [("🤖","Algorithm","Random Forest Regressor"),
                 ("📊","Dataset","5,000 student records"),
                 ("🎯","Test R²","0.83  (83 % explained)"),
                 ("📉","Test MAE","±0.97 pts on average"),
                 ("⚙️","Tuning","GridSearchCV · 5-fold CV")]
        facts_html = ""
        for ic, lb, vl in facts:
            facts_html += f"""
            <div style="display:flex;align-items:center;gap:11px;padding:7px;
                        border-radius:10px;background:rgba(124,58,237,0.06);margin-bottom:5px;">
              <span style="font-size:1.1rem;">{ic}</span>
              <div>
                <div style="font-size:0.64rem;color:#475569;text-transform:uppercase;
                            letter-spacing:0.8px;">{lb}</div>
                <div style="font-size:0.84rem;color:#c4b5fd;font-weight:500;">{vl}</div>
              </div>
            </div>"""
        st.markdown(facts_html, unsafe_allow_html=True)

        st.markdown('<div class="sdiv" style="margin-top:1rem;">Top Predictors</div>',
                    unsafe_allow_html=True)
        for nm, cl, pc in [("Stress Level","#f87171",92),("Sleep Quality","#34d399",75),
                            ("Study Hours","#60a5fa",57),("Screen Time","#fb923c",47),
                            ("Physical Act.","#a78bfa",39),("Daily Unlocks","#f59e0b",32)]:
            st.markdown(f"""
            <div class="bar-row">
              <div class="bl">{nm}</div>
              <div class="bb"><div class="bf"
                   style="width:{pc}%;background:linear-gradient(90deg,{cl}66,{cl});"></div></div>
              <div class="bp">{pc}%</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── PREDICTION ──
        country_group = country_input.strip() if country_input.strip() in TOP_COUNTRIES else "Other"
        df = pd.DataFrame([{
            "Age": age, "Gender": gender, "Country": country_input.strip(),
            "Academic_Level": academic_level, "Most_Used_Platform": most_used_platform,
            "Purpose_Of_Use": purpose_of_use, "Avg_Daily_Usage_Hours": avg_daily_usage_hours,
            "Daily_Unlocks": daily_unlocks, "Study_Hours": study_hours,
            "Physical_Activity_Hours": physical_activity_hours,
            "Sleep_Hours_Per_Night": sleep_hours, "Stress_Level": stress_level,
            "Grouped_country": country_group,
        }])
        with st.spinner("Analysing …"):
            time.sleep(0.3)
            prediction = round(float(model.predict(df)[0]), 2)

        cat, ring_clr, emoji = score_category(prediction)

        # ── Animated SVG gauge via components.html (runs in iframe — JS works!) ──
        gauge_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&family=Inter:wght@400;500&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: rgba(12,12,32,0.0);
    font-family: 'Inter', sans-serif;
    display: flex; align-items: center; justify-content: center;
    min-height: 220px;
    overflow: hidden;
  }}
  .wrap {{
    display: flex; align-items: center; gap: 28px;
    padding: 24px 28px;
    background: rgba(12,12,32,0.82);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 20px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    position: relative; overflow: hidden; width: 100%;
  }}
  .wrap::before {{
    content: ''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, {ring_clr}88, {ring_clr});
    border-radius: 20px 20px 0 0;
  }}
  .ring-box {{ position:relative; flex-shrink:0; width:170px; height:170px; }}
  .ring-box svg {{ transform: rotate(-90deg); width:170px; height:170px; }}
  .ring-center {{
    position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
    text-align:center;
  }}
  .score-num {{
    font-family:'Space Grotesk',sans-serif;
    font-size:2.6rem; font-weight:800; line-height:1; color:#fff;
    background:linear-gradient(135deg,#fff 30%,#c4b5fd 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  }}
  .score-denom {{ font-size:0.78rem; color:#475569; margin-top:3px; }}
  .badge {{
    display:inline-block; margin-top:7px; padding:3px 11px;
    border-radius:100px; font-size:0.75rem; font-weight:700;
    background:{ring_clr}22; color:{ring_clr};
    border:1px solid {ring_clr}55; letter-spacing:0.3px;
  }}
  .info {{ flex:1; min-width:120px; }}
  .info-title {{
    font-family:'Space Grotesk',sans-serif;
    font-size:1.4rem; font-weight:700; color:#fff; line-height:1.25;
    margin-bottom:7px;
  }}
  .info-sub {{ font-size:0.78rem; color:#475569; line-height:1.6; margin-bottom:14px; }}
  .chips {{ display:flex; gap:8px; flex-wrap:wrap; }}
  .chip {{
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
    border-radius:9px; padding:6px 12px;
  }}
  .chip-lbl {{ font-size:0.6rem; color:#475569; text-transform:uppercase; letter-spacing:1px; }}
  .chip-val {{ font-size:0.8rem; font-weight:600; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="ring-box">
    <svg viewBox="0 0 170 170">
      <circle cx="85" cy="85" r="72" fill="none"
              stroke="rgba(255,255,255,0.06)" stroke-width="11"/>
      <circle id="arc" cx="85" cy="85" r="72" fill="none"
              stroke="{ring_clr}" stroke-width="11" stroke-linecap="round"
              stroke-dasharray="452.4" stroke-dashoffset="452.4"
              style="filter:drop-shadow(0 0 8px {ring_clr})"/>
      <circle cx="85" cy="85" r="58" fill="none"
              stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
    </svg>
    <div class="ring-center">
      <div class="score-num" id="snum">0.00</div>
      <div class="score-denom">/ 10</div>
      <div class="badge">{emoji} {cat}</div>
    </div>
  </div>
  <div class="info">
    <div class="info-title">Mental Health<br/>Score</div>
    <div class="info-sub">Based on your lifestyle,<br/>social media & stress inputs</div>
    <div class="chips">
      <div class="chip">
        <div class="chip-lbl">Model</div>
        <div class="chip-val" style="color:#a78bfa;">Random Forest</div>
      </div>
      <div class="chip">
        <div class="chip-lbl">Accuracy</div>
        <div class="chip-val" style="color:#34d399;">R² = 0.83</div>
      </div>
    </div>
  </div>
</div>
<script>
  var arc  = document.getElementById('arc');
  var snum = document.getElementById('snum');
  var C = 452.4, target = {prediction}, dur = 1300, start = null;
  function ease(t) {{ return 1 - Math.pow(1-t, 3); }}
  function tick(ts) {{
    if (!start) start = ts;
    var p = Math.min((ts-start)/dur, 1), e = ease(p);
    arc.style.strokeDashoffset = C - e*(C - C*(1-target/10));
    snum.textContent = (e*target).toFixed(2);
    if (p < 1) requestAnimationFrame(tick);
    else snum.textContent = target.toFixed(2);
  }}
  requestAnimationFrame(tick);
</script>
</body>
</html>
"""
        components.html(gauge_html, height=230, scrolling=False)

        # ── Metric tiles ──
        sc = "#34d399" if sleep_hours >= 7 else ("#facc15" if sleep_hours >= 6 else "#f87171")
        mc = "#34d399" if avg_daily_usage_hours <= 2 else ("#facc15" if avg_daily_usage_hours <= 4 else "#f87171")
        ac = "#34d399" if physical_activity_hours >= 1 else ("#facc15" if physical_activity_hours >= 0.5 else "#f87171")
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-box">
            <div class="m-icon">😴</div>
            <div class="m-val" style="color:{sc};">{sleep_hours}h</div>
            <div class="m-lbl">Sleep</div>
          </div>
          <div class="metric-box">
            <div class="m-icon">📱</div>
            <div class="m-val" style="color:{mc};">{avg_daily_usage_hours}h</div>
            <div class="m-lbl">Screen Time</div>
          </div>
          <div class="metric-box">
            <div class="m-icon">🏃</div>
            <div class="m-val" style="color:{ac};">{physical_activity_hours}h</div>
            <div class="m-lbl">Activity</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Tips + bars in two sub-cols ──
        tc1, tc2 = st.columns([1.1, 1])

        with tc1:
            st.markdown('<div class="sdiv">💡 Wellness Tips</div>', unsafe_allow_html=True)
            tips = []
            if sleep_hours < 7:
                tips.append(("😴","Improve Sleep",
                    f"Only {sleep_hours}h — target 7–9h. Poor sleep is the biggest risk factor."))
            if avg_daily_usage_hours > 4:
                tips.append(("📵","Cut Screen Time",
                    f"{avg_daily_usage_hours}h/day is too high. Use app timers or grayscale mode."))
            if physical_activity_hours < 0.5:
                tips.append(("🏃","Exercise Daily",
                    "Even 20-min walks release endorphins that counter anxiety."))
            if stress_level in ("High","Very High"):
                tips.append(("🧘","Manage Stress",
                    "Try box breathing (4-4-4-4) or speak to your campus counsellor."))
            if study_hours > 10:
                tips.append(("📚","Avoid Burnout",
                    f"{study_hours}h is unsustainable. Try Pomodoro: 25 min on, 5 off."))
            if not tips:
                tips.append(("🌟","Great Habits!",
                    "Your routine looks healthy — stay consistent and keep social connections."))

            for i,(em,h,p) in enumerate(tips):
                st.markdown(f"""
                <div class="tip-card" style="animation-delay:{i*0.07}s;">
                  <div class="t-em">{em}</div>
                  <div>
                    <div class="t-h">{h}</div>
                    <div class="t-p">{p}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with tc2:
            st.markdown('<div class="sdiv">📊 Your Factor Breakdown</div>', unsafe_allow_html=True)
            stress_p = {"Low":18,"Medium":45,"High":72,"Very High":95}[stress_level]
            for nm, cl, pc in [
                ("Stress",   "#f87171", stress_p),
                ("Sleep",    "#34d399", min(int(sleep_hours/12*100),100)),
                ("Study",    "#60a5fa", min(int(study_hours/16*100),100)),
                ("Screen",   "#fb923c", min(int(avg_daily_usage_hours/12*100),100)),
                ("Activity", "#a78bfa", min(int(physical_activity_hours/8*100),100)),
            ]:
                st.markdown(f"""
                <div class="bar-row">
                  <div class="bl">{nm}</div>
                  <div class="bb"><div class="bf"
                       style="width:{pc}%;background:linear-gradient(90deg,{cl}55,{cl});"></div></div>
                  <div class="bp">{pc}%</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="sdiv" style="margin-top:0.9rem;">🗺 Score Guide</div>',
                        unsafe_allow_html=True)
            for rng, lbl, cl in [("8.0 – 10","Excellent 🌟","#00d4aa"),
                                  ("6.5 – 7.9","Good 😊","#4ade80"),
                                  ("5.0 – 6.4","Moderate 😐","#facc15"),
                                  ("3.5 – 4.9","Low 😟","#fb923c"),
                                  ("0 – 3.4","Poor 😔","#f87171")]:
                st.markdown(f"""
                <div class="gr">
                  <span style="font-size:0.75rem;color:#64748b;">{rng}</span>
                  <span style="font-size:0.77rem;font-weight:600;color:{cl};">{lbl}</span>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────── FOOTER ───────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.2rem;margin-top:1rem;
            background:rgba(12,12,32,0.55);border:1px solid rgba(255,255,255,0.05);
            border-radius:14px;backdrop-filter:blur(10px);">
  <span style="font-size:0.77rem;color:#374151;">
    🧠 <strong style="color:#7c3aed;">MindScore</strong> &nbsp;·&nbsp;
    Random Forest Pipeline &nbsp;·&nbsp;
    Part 3 – Streamlit Deployment &nbsp;·&nbsp;
    Applied Machine Learning &nbsp;·&nbsp; R² = 0.83
  </span>
</div>
""", unsafe_allow_html=True)
