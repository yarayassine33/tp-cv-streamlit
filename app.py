"""
STREAMLIT CV + Course - Dataset above
Yara YASSINE - EFREI Paris - BDML2 - 2026-2027
Professeur : MATHEW Mano Joseph
"""
import base64
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).parent
ASSETS = BASE / "assets"
DATA_URL = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"

NAVY, ORANGE, YELLOW = "#1B2A49", "#FF6B35", "#FFC857"
TEAL, PINK, PURPLE = "#2EC4B6", "#FF8FA3", "#6C4AB6"

st.set_page_config(
    page_title="Yara Yassine · CV + NYC Taxi",
    page_icon="🚕",
    layout="wide",
)

# --------------------------------------------------------------------------
# Petits outils
# --------------------------------------------------------------------------
def html(s: str) -> None:
    """Affiche du HTML (on retire l'indentation pour éviter le mode 'code' du markdown)."""
    st.markdown(" ".join(line.strip() for line in s.splitlines() if line.strip()), unsafe_allow_html=True)


def show_fig(fig) -> None:
    """Affiche une figure plotly (compatible anciennes et nouvelles versions de Streamlit)."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def show_df(df: pd.DataFrame) -> None:
    try:
        st.dataframe(df, width="stretch")
    except TypeError:
        st.dataframe(df, use_container_width=True)


def img_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def insight(text: str) -> None:
    html(f'<div class="insight"><span>💡</span><div>{text}</div></div>')


JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def fr_date(d: dt.date) -> str:
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]} {d.year}"


# --------------------------------------------------------------------------
# Style
# --------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"], .stMarkdown, p, li, label { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, .fun { font-family: 'Fredoka', sans-serif !important; letter-spacing: .2px; }
h2 { margin-top: 1.6rem !important; }

/* onglets */
.stTabs [role="tablist"] { gap: 8px; }
.stTabs [role="tab"] {
  padding: 10px 20px; border-radius: 14px 14px 0 0; background: #FFE9D6; height:auto;
}
.stTabs [role="tab"] p { font-family: 'Fredoka', sans-serif; font-size: 1.1rem; font-weight: 600; }
.stTabs [role="tab"][aria-selected="true"] { background: #1B2A49 !important; }
.stTabs [role="tab"][aria-selected="true"] p { color: #FFF8F0 !important; }

/* sidebar */
.logo-fallback { font-family:'Fredoka',sans-serif; font-weight:700; font-size:2rem; color:#1B2A49; }
.logo-fallback span { color:#FF6B35; }
.id-card {
  background:#1B2A49; color:#FFF8F0; border-radius:20px; padding:16px 18px; margin-top:12px;
  box-shadow:5px 5px 0 #FF6B35; font-size:.88rem; line-height:1.5;
}
.id-card .lbl { color:#FFC857; font-family:'Fredoka',sans-serif; font-size:.78rem; text-transform:uppercase; letter-spacing:1px; margin-top:10px; }
.id-card .val { font-weight:600; word-break:break-word; }
.id-card a { color:#FFF8F0 !important; text-decoration:underline dotted; }

/* hero */
.hero {
  position:relative; overflow:hidden; border-radius:32px; padding:34px 40px; color:#fff;
  background: linear-gradient(135deg, #1B2A49 0%, #3D2C8D 55%, #FF6B35 135%);
  display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;
  box-shadow:8px 8px 0 #FFC857;
}
.hero h1 { color:#fff; font-size:3.2rem; margin:0; line-height:1.05; }
.hero .hello { font-family:'Fredoka',sans-serif; font-size:1.3rem; color:#FFC857; }
.hero .tagline { font-size:1.15rem; margin:.6rem 0 1rem 0; max-width:560px; }
.chip {
  display:inline-block; padding:5px 14px; margin:3px 6px 3px 0; border-radius:999px; font-size:.85rem;
  background:rgba(255,255,255,.16); border:1.5px solid rgba(255,255,255,.45); color:#fff; font-weight:500;
}
.hero > div:first-of-type { flex:1 1 420px; min-width:0; z-index:2; }
.avatar { flex:0 0 auto; width:190px; height:190px; border-radius:50%; object-fit:cover; object-position:center 20%;
  border:6px solid #FFC857; box-shadow:0 0 0 6px rgba(255,255,255,.25); z-index:2; }
.floaty { position:absolute; font-size:2rem; opacity:.85; animation: bob 4s ease-in-out infinite; z-index:1; }
@keyframes bob { 0%,100% { transform:translateY(0) rotate(-6deg);} 50% { transform:translateY(-14px) rotate(6deg);} }

/* bulle de profil */
.bubble { position:relative; background:#fff; border:3px solid #1B2A49; border-radius:22px; padding:18px 22px;
  margin:26px 0 8px 0; box-shadow:6px 6px 0 #2EC4B6; font-size:1.02rem; }
.bubble:before { content:'💬'; position:absolute; top:-20px; left:22px; font-size:1.6rem; background:#FFF8F0; border-radius:50%; }

/* cartes stats / quêtes */
.stat { background:#fff; border:3px solid #1B2A49; border-radius:20px; padding:16px; text-align:center;
  box-shadow:6px 6px 0 #1B2A49; transition: transform .15s; }
.stat:hover { transform: translate(-3px,-3px) rotate(-1deg); }
.stat .big { font-family:'Fredoka',sans-serif; font-size:2.4rem; font-weight:700; line-height:1.1; }
.stat .sm { font-size:.9rem; color:#4a557a; }

.quest { background:#fff; border:3px solid #1B2A49; border-radius:20px; padding:18px; height:100%;
  box-shadow:6px 6px 0 var(--c); transition: transform .15s; min-height:275px; }
.quest:hover { transform: translate(-3px,-3px) rotate(1deg); }
.quest .emo { font-size:2.4rem; }
.quest .ttl { font-family:'Fredoka',sans-serif; font-weight:600; font-size:1.25rem; margin:.2rem 0; }
.quest .yr { display:inline-block; background:var(--c); color:#1B2A49; border-radius:999px; padding:2px 12px; font-size:.8rem; font-weight:600; }
.quest p { font-size:.93rem; margin:.6rem 0 0 0; }
.quest.next { border-style:dashed; background:#FFF3C4; }

.job { background:#fff; border:3px solid #1B2A49; border-left:14px solid #FF6B35; border-radius:20px; padding:18px 24px;
  box-shadow:6px 6px 0 #1B2A49; }
.job .role { font-family:'Fredoka',sans-serif; font-size:1.3rem; font-weight:600; }
.job .when { color:#FF6B35; font-weight:600; }

.skill { display:inline-block; padding:6px 14px; margin:4px 6px 4px 0; border-radius:12px; font-weight:600; font-size:.9rem;
  border:2px solid #1B2A49; background:var(--c); color:#1B2A49; }
.skillrow .grp { font-family:'Fredoka',sans-serif; font-size:1.05rem; margin:12px 0 2px 0; }

.lang { display:flex; justify-content:space-between; align-items:center; background:#fff; border:2px solid #1B2A49;
  border-radius:14px; padding:8px 16px; margin:6px 0; }
.dots { letter-spacing:3px; color:#FF6B35; font-size:1.1rem; }

.mission { background:#1B2A49; color:#FFF8F0; border-radius:24px; padding:22px 28px; margin-top:18px;
  box-shadow:8px 8px 0 #FF6B35; font-size:1.05rem; }
.mission b { color:#FFC857; }

/* TP */
.insight { display:flex; gap:12px; align-items:flex-start; background:#FFF3C4; border:2.5px solid #1B2A49;
  border-radius:16px; padding:12px 16px; margin:10px 0 22px 0; box-shadow:4px 4px 0 #FFC857; }
.insight span { font-size:1.4rem; }

[data-testid="stMetric"] { background:#fff; border:3px solid #1B2A49; border-radius:18px; padding:12px 16px;
  box-shadow:5px 5px 0 #FFC857; }
[data-testid="stMetricValue"] { font-family:'Fredoka',sans-serif; }

.story { background:#fff; border:3px solid #1B2A49; border-radius:20px; padding:18px 20px; height:100%;
  box-shadow:6px 6px 0 var(--c); }
.story h4 { margin-top:0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Données (mêmes étapes que le notebook)
# --------------------------------------------------------------------------
@st.cache_data(show_spinner="Chargement du dataset NYC Taxi…")
def load_raw() -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_URL, delimiter=",")
    except Exception:  # pas d'internet -> copie locale
        df = pd.read_csv(BASE / "data" / "data.csv", delimiter=",")
    df["pickup"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.tz_localize(None)
    df["dropoff"] = pd.to_datetime(df["tpep_dropoff_datetime"]).dt.tz_localize(None)
    df["duration_min"] = (df["dropoff"] - df["pickup"]).dt.total_seconds() / 60
    df["hour"] = df["pickup"].dt.hour
    df["day_name"] = df["pickup"].dt.day_name()
    return df


@st.cache_data(show_spinner=False)
def clean(df2: pd.DataFrame):
    """Retourne (df_clean, tableau des critères)."""
    in_nyc = (
        df2["pickup_longitude"].between(-74.3, -73.7)
        & df2["pickup_latitude"].between(40.5, 41.0)
        & df2["dropoff_longitude"].between(-74.3, -73.7)
        & df2["dropoff_latitude"].between(40.5, 41.0)
    )
    ok_dur = (df2["duration_min"] > 0) & (df2["duration_min"] <= 180)
    ok_dist = (df2["trip_distance"] > 0) & (df2["trip_distance"] <= 50)
    ok_pass = df2["passenger_count"] > 0
    ok_fare = df2["fare_amount"] > 0
    valid = ok_dur & ok_dist & ok_pass & ok_fare & in_nyc

    df_clean = df2[valid].copy()
    df_clean["speed_mph"] = df_clean["trip_distance"] / (df_clean["duration_min"] / 60)
    n_fast = int((df_clean["speed_mph"] > 100).sum())
    df_clean = df_clean[df_clean["speed_mph"] <= 100].copy()

    criteria = pd.DataFrame(
        {
            "Critère invalide": [
                "Durée ≤ 0 ou > 180 min",
                "Distance ≤ 0 ou > 50 miles",
                "0 passager",
                "Tarif ≤ 0",
                "GPS hors de New York",
                "Vitesse > 100 mph (après les autres filtres)",
            ],
            "Trajets concernés": [
                int((~ok_dur).sum()),
                int((~ok_dist).sum()),
                int((~ok_pass).sum()),
                int((~ok_fare).sum()),
                int((~in_nyc).sum()),
                n_fast,
            ],
        }
    )
    return df_clean, criteria


raw = load_raw()
df_clean, criteria = clean(raw)
trips_per_hour = df_clean["hour"].value_counts().sort_index()
top3 = trips_per_hour.sort_values(ascending=False).head(3)
peak_hour = int(trips_per_hour.idxmax())
corr = df_clean[["trip_distance", "duration_min"]].corr().iloc[0, 1]
days = raw["pickup"].dt.date.unique()
date_label = fr_date(days[0]) if len(days) == 1 else f"du {days.min()} au {days.max()}"


# --------------------------------------------------------------------------
# Sidebar : logo + identité
# --------------------------------------------------------------------------
with st.sidebar:
    logo = next(iter(sorted(ASSETS.glob("logo_efrei.*"))), None)
    if logo is not None:
        try:
            st.image(str(logo), width="stretch")
        except TypeError:
            st.image(str(logo), use_container_width=True)
    else:
        html('<div class="logo-fallback">EFREI<span> Paris</span></div>')

    html("""
    <div class="id-card">
      <div class="lbl">Étudiante</div><div class="val">YASSINE Yara</div>
      <div class="val"><a href="mailto:yara.yassine@efrei.net">yara.yassine@efrei.net</a></div>
      <div class="lbl">Cours</div><div class="val">STREAMLIT CV + Course - Dataset above</div>
      <div class="lbl">Professeur</div><div class="val">MATHEW Mano Joseph</div>
      <div class="val"><a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a></div>
      <div class="lbl">Classe</div><div class="val">BDML2</div>
      <div class="lbl">Année</div><div class="val">2026-2027</div>
    </div>
    """)
    st.write("")
    st.caption("🚕 Dataset : NYC taxi trips (kepler.gl) · 15 janvier 2015")


# --------------------------------------------------------------------------
# Onglets principaux
# --------------------------------------------------------------------------
tab_cv, tab_tp = st.tabs(["🎨 Mon CV (version fun)", "🚕 Cours · TP DataViz NYC Taxi"])

# ==========================================================================
# ONGLET 1 : CV
# ==========================================================================
with tab_cv:
    photo = img_b64(ASSETS / "photo_yara.jpg")
    html(
        f"""
        <div class="hero">
          <span class="floaty" style="top:12px; left:46%; animation-delay:0s;">📊</span>
          <span class="floaty" style="bottom:14px; left:38%; animation-delay:.8s;">🤖</span>
          <span class="floaty" style="top:18px; right:28%; animation-delay:1.6s;">🚀</span>
          <span class="floaty" style="bottom:20px; right:24%; animation-delay:2.4s;">🌍</span>
          <div>
            <div class="hello">👋 Hi, I'm</div>
            <h1>Yara Yassine</h1>
            <div class="tagline">Engineering student in <b>Big Data &amp; Machine Learning</b> — turning messy data into decisions.</div>
            <span class="chip">🎓 EFREI Paris · 2023–2028</span>
            <span class="chip">💼 Data Analyst (work-study)</span>
            <span class="chip">🌍 Open to an international exchange 2027–2028</span>
          </div>
          <img class="avatar" src="data:image/jpeg;base64,{photo}" alt="Yara Yassine"/>
        </div>
        """
    )

    html(
        """
        <div class="bubble">Engineering student in Big Data and Machine Learning with a strong academic record and a solid
        mathematical background. Hands-on experience in data engineering and business intelligence (Snowflake, SQL, Power BI)
        through a work-study position at Fayat IT. Looking to deepen my knowledge of AI and data science abroad, with the goal
        of becoming an <b>AI Product Owner</b> in a large group.</div>
        """
    )

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (c1, "Top 15%", "of the preparatory cycle", ORANGE),
        (c2, "885", "TOEIC score", TEAL),
        (c3, "4", "languages (FR · EN · AR · PT)", PURPLE),
        (c4, "5", "projects built so far", PINK),
    ]
    for col, big, small, color in stats:
        with col:
            html(f'<div class="stat"><div class="big" style="color:{color}">{big}</div><div class="sm">{small}</div></div>')

    # ---- Timeline ----
    st.header("🗺️ My journey so far")
    today = pd.Timestamp(dt.date.today())
    tl = pd.DataFrame(
        [
            ("EFREI Paris · Engineering degree", "2023-01-01", "2028-12-31", "Education", "2023 – 2028"),
            ("Fayat IT · Data Analyst (work-study)", "2025-09-01", today, "Work", "Sept 2025 – present"),
            ("EFREI Aides Humanitaires · Volunteer", "2024-09-01", today, "Volunteering", "Sept 2024 – present"),
            ("Wine Quality Classification", "2026-01-01", "2026-12-31", "Project", "2026"),
            ("DATABANQUE", "2025-01-01", "2025-12-31", "Project", "2025"),
            ("Rover Run", "2024-01-01", "2025-12-31", "Project", "2024 – 2025"),
            ("CDataframe", "2024-01-01", "2024-12-31", "Project", "2024"),
            ("ChatBot", "2023-01-01", "2023-12-31", "Project", "2023"),
        ],
        columns=["Item", "Start", "Finish", "Type", "Period"],
    )
    tl["Start"] = pd.to_datetime(tl["Start"])
    tl["Finish"] = pd.to_datetime(tl["Finish"])
    fig_tl = px.timeline(
        tl, x_start="Start", x_end="Finish", y="Item", color="Type",
        color_discrete_map={"Education": NAVY, "Work": ORANGE, "Volunteering": TEAL, "Project": PURPLE},
        hover_name="Item", hover_data={"Start": False, "Finish": False, "Item": False, "Period": True, "Type": False},
    )
    fig_tl.update_yaxes(autorange="reversed", title=None)
    fig_tl.update_xaxes(title=None)
    fig_tl.add_shape(type="line", x0=today, x1=today, y0=0, y1=1, yref="paper",
                     line=dict(color=ORANGE, width=2, dash="dot"))
    fig_tl.add_annotation(x=today, y=1.0, yref="paper", text="Today", showarrow=False,
                          yanchor="bottom", font=dict(color=ORANGE))
    fig_tl.update_layout(height=420, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         legend_title_text="", margin=dict(l=0, r=0, t=30, b=0),
                         font=dict(family="Inter"))
    show_fig(fig_tl)
    st.caption("Bars are approximate (year precision) · hover a bar for the exact period.")

    # ---- Experience ----
    st.header("💼 Experience")
    html(
        """
        <div class="job">
          <div class="role">Data Analyst (work-study) · Fayat IT (Fayat Group)</div>
          <div class="when">Sept 2025 – present · Data &amp; Integration team</div>
          <ul>
            <li>Built <b>Power BI</b> dashboards used in management meetings: KPIs defined with stakeholders and implemented in DAX.</li>
            <li>Developed dashboards to manage the accounts of departed employees and mobile device management (MDM).</li>
            <li>Mapped data flows between MuleSoft, Talend, GoAnywhere and Snowflake; restructured nested JSON into working tables.</li>
            <li>Wrote advanced <b>SQL on Snowflake</b> (CTEs, joins, JSON parsing); built a centralised view of IT support activity from Matrix42 tickets.</li>
          </ul>
        </div>
        """
    )

    # ---- Quests (projects) ----
    st.header("🎮 Quests completed (projects)")
    quests = [
        ("🍷", "Wine Quality Classification", "2026", TEAL,
         "Machine Learning · team of 3. Built a model that predicts whether a wine is good from its chemical measurements (6,497 wines). Tested four approaches and kept the most accurate one."),
        ("🏦", "DATABANQUE", "2025", YELLOW,
         "Designed and implemented an optimised relational database (E/R model, normalisation, complex SQL queries) to manage a real-life project."),
        ("🚀", "Rover Run", "2024 – 2025", ORANGE,
         "Developed an algorithm in C optimising the movements of a Mars rover, with advanced data structures and efficient memory management."),
        ("🐼", "CDataframe", "2024", PINK,
         "Designed a C library inspired by Pandas for advanced manipulation of tabular data. Optimised operations on dynamic structures and handled CSV exports."),
        ("🤖", "ChatBot", "2023", PURPLE,
         "Implemented a Python chatbot based on TF-IDF for automatic language processing, with information retrieval models and user interaction handling."),
    ]
    cols = st.columns(3)
    for i, (emo, ttl, yr, color, desc) in enumerate(quests):
        with cols[i % 3]:
            html(
                f'<div class="quest" style="--c:{color}"><div class="emo">{emo}</div>'
                f'<div class="ttl">{ttl}</div><span class="yr">{yr}</span><p>{desc}</p></div>'
            )
            st.write("")
    with cols[2]:
        html(
            '<div class="quest next" style="--c:#FFC857"><div class="emo">🌍</div>'
            '<div class="ttl">Next quest: international exchange</div><span class="yr">2027 – 2028</span>'
            '<p>Deepen my knowledge of AI and data science abroad. Loading… ⏳</p></div>'
        )

    # ---- Skills & languages ----
    left, right = st.columns([3, 2])
    with left:
        st.header("🧰 Skill tree")
        groups = [
            ("📊 Data", ["Snowflake", "SQL", "Power BI (DAX)", "Data modelling", "JSON"], ORANGE),
            ("🔌 Integration", ["Talend", "MuleSoft", "GoAnywhere", "Matrix42", "Azure", "SharePoint"], TEAL),
            ("💻 Programming", ["Python", "C", "Java", "Scala", "MySQL"], YELLOW),
            ("🧠 Machine learning & AI", ["Machine Learning I & II", "Deep Learning", "Maths for Data Scientists", "Convex Optimization"], PINK),
            ("☁️ Big data & cloud", ["Big Data Frameworks", "NoSQL databases", "Datalakes", "Data Integration", "Cloud Computing", "DevOps & MLOps"], "#B9A6F2"),
        ]
        out = '<div class="skillrow">'
        for name, items, color in groups:
            out += f'<div class="grp">{name}</div>'
            out += "".join(f'<span class="skill" style="--c:{color}">{s}</span>' for s in items)
        out += "</div>"
        html(out)
    with right:
        st.header("🗣️ Languages")
        langs = [("🇫🇷 French", "Fluent", 5), ("🇬🇧 English", "Fluent · TOEIC 885", 5),
                 ("🇸🇦 Arabic", "Fluent", 5), ("🇧🇷 Portuguese (Brazil)", "Beginner, learning", 1)]
        out = ""
        for name, lvl, n in langs:
            dots = "●" * n + "○" * (5 - n)
            out += f'<div class="lang"><div><b>{name}</b><br><small>{lvl}</small></div><div class="dots">{dots}</div></div>'
        html(out)

        st.header("🤝 Beyond the screen")
        html(
            '<div class="lang" style="display:block"><b>EFREI Aides Humanitaires</b> · Volunteer · Sept 2024 – present<br>'
            '<small>Association helping people in need: participation in <i>maraudes</i> (street outreach rounds '
            'distributing meals) and in various events.</small></div>'
        )

    html(
        """
        <div class="mission">🎯 <b>Mission:</b> an international exchange in 2027–2028 to dive deeper into AI &amp; data science,
        then become an <b>AI Product Owner</b> in a large group.</div>
        """
    )
    st.write("")
    b1, b2, b3, b4 = st.columns([1.2, 1.2, 1.2, 1])
    with b1:
        if st.button("🎉 Hire Yara!", type="primary"):
            st.balloons()
            st.success("Great choice! Write to **yara.yassine@efrei.net** 💌")
    with b2:
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/yara-yassine")
    with b3:
        st.link_button("✉️ Send an email", "mailto:yara.yassine@efrei.net")
    with b4:
        st.download_button("📄 Download CV (PDF)", (ASSETS / "CV_Yara_Yassine.pdf").read_bytes(),
                           file_name="CV_Yara_Yassine.pdf", mime="application/pdf")

# ==========================================================================
# ONGLET 2 : TP DataViz
# ==========================================================================
with tab_tp:
    st.title("🚕 TP DataViz : NYC Taxi Trips")
    st.write(
        "Analyse de la demande de taxis à New York : chargement, nettoyage, statistiques, "
        "visualisations dynamiques, KPI et storytelling."
    )
    nb_path = BASE / "notebook" / "DataViz_20000_YASSINE2026BDML2.ipynb"
    if nb_path.exists():
        st.download_button("📓 Télécharger le notebook (.ipynb)", nb_path.read_bytes(),
                           file_name=nb_path.name, mime="application/x-ipynb+json")

    t1, t2, t3, t4, t5 = st.tabs(
        ["1 · Données", "2 · Nettoyage", "3 · Statistiques", "4 · Dynamique + KPI", "5 · Storytelling"]
    )

    # ---------- 1. Données ----------
    with t1:
        st.header("Chargement des données")
        m1, m2, m3 = st.columns(3)
        m1.metric("Lignes", f"{len(raw):,}".replace(",", " "))
        m2.metric("Colonnes (brutes)", 12)
        m3.metric("Date des trajets", f"{days[0]:%d/%m/%Y}" if len(days) == 1 else f"{days.min()} → {days.max()}")
        st.subheader("Aperçu")
        show_df(raw.head(10))

        st.header("Valeurs manquantes (missingno)")
        base_cols = [c for c in raw.columns[:12]]
        try:
            import matplotlib.pyplot as plt
            import missingno as msno

            ax = msno.bar(raw[base_cols], figsize=(10, 4), color="#FF6B35", fontsize=9)
            st.pyplot(ax.figure)
            plt.close(ax.figure)
        except Exception:
            miss = raw[base_cols].isna().mean().mul(100).rename("% manquant").reset_index()
            show_fig(px.bar(miss, x="index", y="% manquant", color_discrete_sequence=[ORANGE]))
        nb_nan = int(raw[base_cols].isna().sum().sum())
        insight(
            f"<b>{nb_nan} valeur manquante</b> dans le dataset : toutes les colonnes sont complètes. "
            "Mais l'absence de NaN ne garantit pas la qualité : des valeurs invalides "
            "(distances nulles, durées négatives, GPS hors de New York…) sont traitées à l'étape suivante."
        )

    # ---------- 2. Nettoyage ----------
    with t2:
        st.header("Nettoyage et préparation")
        n0, n1 = len(raw), len(df_clean)
        k1, k2, k3 = st.columns(3)
        k1.metric("Avant nettoyage", f"{n0:,}".replace(",", " "))
        k2.metric("Après nettoyage", f"{n1:,}".replace(",", " "))
        k3.metric("Supprimés", f"{n0 - n1:,}".replace(",", " "), f"-{(n0 - n1) / n0:.2%}", delta_color="off")

        st.subheader("Préparation")
        st.markdown(
            "- Dates converties en `datetime` (`pickup`, `dropoff`)\n"
            "- `duration_min` = durée du trajet en minutes\n"
            "- `hour` = heure de départ · `day_name` = jour de la semaine\n"
            "- `speed_mph` = vitesse moyenne (distance / durée)"
        )
        st.subheader("Critères de suppression")
        fig_c = px.bar(criteria, x="Trajets concernés", y="Critère invalide", orientation="h",
                       text="Trajets concernés", color_discrete_sequence=[ORANGE])
        fig_c.update_yaxes(autorange="reversed", title=None)
        fig_c.update_layout(height=340, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0, r=0, t=10, b=0))
        show_fig(fig_c)
        insight(
            "Un même trajet peut cumuler plusieurs problèmes : la somme des barres est donc supérieure "
            "au nombre de lignes supprimées. Seuls <b>environ 0,7 %</b> des trajets sont retirés."
        )
        st.subheader("Données nettoyées")
        show_df(df_clean[["pickup", "dropoff", "duration_min", "hour", "trip_distance", "speed_mph",
                          "passenger_count", "fare_amount", "tip_amount"]].head(10))

    # ---------- 3. Statistiques ----------
    with t3:
        st.header("📊 Distribution des distances")
        nbins = st.slider("Nombre de barres", 10, 100, 50, key="bins")
        med, mean = df_clean["trip_distance"].median(), df_clean["trip_distance"].mean()
        fig_h = px.histogram(df_clean, x="trip_distance", nbins=nbins, color_discrete_sequence=[NAVY],
                             labels={"trip_distance": "Distance (miles)"})
        fig_h.add_vline(x=med, line_dash="dash", line_color=ORANGE, annotation_text=f"médiane {med:.2f}",
                        annotation_position="top left")
        fig_h.add_vline(x=mean, line_dash="dot", line_color=TEAL, annotation_text=f"moyenne {mean:.2f}",
                        annotation_position="top right")
        fig_h.update_layout(yaxis_title="Nombre de trajets", bargap=0.05, height=430,
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        show_fig(fig_h)
        q75 = df_clean["trip_distance"].quantile(0.75)
        insight(
            f"La plupart des trajets sont courts. La médiane est de <b>{med:.2f} mile</b> et 75 % des trajets font "
            f"moins de <b>{q75:.2f} miles</b>. Quelques trajets très longs (jusqu'à {df_clean['trip_distance'].max():.2f} miles) "
            f"font monter la moyenne à {mean:.2f} miles."
        )
        with st.expander("Voir le tableau describe()"):
            show_df(df_clean["trip_distance"].describe().to_frame().T)

        st.header("🕒 Trajets par heure de la journée")
        colors = [ORANGE if h in top3.index else NAVY for h in trips_per_hour.index]
        fig_b = go.Figure(go.Bar(x=trips_per_hour.index, y=trips_per_hour.values, marker_color=colors,
                                 hovertemplate="%{x} h : %{y} trajets<extra></extra>"))
        fig_b.update_layout(xaxis=dict(title="Heure de départ (0 à 23)", dtick=1), yaxis_title="Nombre de trajets",
                            height=430, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        show_fig(fig_b)
        tops = ", ".join(f"{h} h" for h in sorted(top3.index))
        insight(
            f"La demande est la plus forte en soirée, avec des pics à <b>{tops}</b> (en orange). "
            f"Cela correspond probablement au retour du travail, puis aux sorties du soir. "
            f"Les données ne couvrent qu'une journée ({date_label}) : ce profil est celui d'un jeudi."
        )

    # ---------- 5. Storytelling ----------
    with t5:
        st.header("📖 Ce que racontent les taxis de New York")
        st.write(
            f"**Le contexte.** {len(df_clean):,} trajets valides (après nettoyage), effectués {date_label}.".replace(",", " ")
        )
        s1, s2, s3 = st.columns(3)
        with s1:
            html(
                f'<div class="story" style="--c:{ORANGE}"><h4>🕒 Dans le temps</h4>'
                f"La demande est la plus forte en soirée, avec des pics à {', '.join(f'{h} h' for h in sorted(top3.index))} : "
                "retour du travail puis sorties du soir. Elle est la plus faible la nuit.</div>"
            )
        with s2:
            html(
                f'<div class="story" style="--c:{TEAL}"><h4>📍 Dans l\'espace</h4>'
                "Les départs sont concentrés à Manhattan, surtout dans le centre. "
                "Les aéroports JFK et LaGuardia forment deux petits points chauds isolés.</div>"
            )
        with s3:
            html(
                f'<div class="story" style="--c:{PURPLE}"><h4>🚕 Les trajets</h4>'
                f"Le taxi sert surtout à de courts déplacements : médiane de {med:.2f} mile, "
                f"75 % des trajets sous {q75:.2f} miles. Un trajet moyen dure {df_clean['duration_min'].mean():.0f} minutes "
                f"et coûte {df_clean['fare_amount'].mean():.2f} dollars.</div>"
            )
        st.write("")
        st.markdown(
            f"**La circulation.** La durée augmente avec la distance (corrélation de {corr:.2f}), mais elle varie beaucoup "
            f"pour une même distance. La vitesse moyenne n'est que de {df_clean['speed_mph'].mean():.1f} mph : "
            "la congestion ralentit les taxis."
        )

        st.subheader("🎯 Recommandations (vision BI)")
        st.markdown(
            "- Renforcer le nombre de taxis disponibles en soirée (19 h à 22 h), quand la demande est la plus forte.\n"
            "- Concentrer l'offre à Manhattan, et prévoir une présence aux aéroports pour les courses longues et plus rentables.\n"
            "- Tenir compte de la congestion dans la planification : un trajet de même distance peut durer très "
            "différemment selon l'heure."
        )
        st.subheader("⚠️ Limites")
        st.markdown(
            f"Les données couvrent une seule journée ({date_label}) : les conclusions décrivent un jeudi de janvier "
            "et ne peuvent pas être généralisées à toute l'année. Le pourboire moyen peut aussi être sous-estimé si "
            "les pourboires en espèces ne sont pas enregistrés."
        )

    # ---------- 4. Dynamique + KPI ----------
    with t4:
        st.header("🎛️ Filtres")
        f1, f2, f3, f4 = st.columns(4)
        hours = f1.slider("Heures de départ", 0, 23, (0, 23))
        dmax = f2.slider("Distance max (miles)", 1, 50, 50)
        pax = f3.multiselect("Passagers", sorted(df_clean["passenger_count"].unique()),
                             default=sorted(df_clean["passenger_count"].unique()))
        n_sample = f4.slider("Taille de l'échantillon", 1000, 20000, 5000, step=1000)

        sel = df_clean[
            df_clean["hour"].between(*hours)
            & (df_clean["trip_distance"] <= dmax)
            & df_clean["passenger_count"].isin(pax)
        ]
        if sel.empty:
            st.warning("Aucun trajet ne correspond à ces filtres.")
            st.stop()

        st.header("📈 KPI")
        peak_sel = int(sel["hour"].value_counts().idxmax())
        tip_rate = sel["tip_amount"].sum() / sel["fare_amount"].sum()
        r1 = st.columns(4)
        r1[0].metric("Nombre de trajets", f"{len(sel):,}".replace(",", " "))
        r1[1].metric("Distance moyenne", f"{sel['trip_distance'].mean():.2f} mi")
        r1[2].metric("Durée moyenne", f"{sel['duration_min'].mean():.1f} min")
        r1[3].metric("Vitesse moyenne", f"{sel['speed_mph'].mean():.1f} mph")
        r2 = st.columns(4)
        r2[0].metric("Tarif moyen", f"{sel['fare_amount'].mean():.2f} $")
        r2[1].metric("Pourboire moyen", f"{sel['tip_amount'].mean():.2f} $")
        r2[2].metric("Pourboire / tarif", f"{tip_rate:.1%}")
        r2[3].metric("Heure de pointe", f"{peak_sel} h")

        smp = sel.sample(min(n_sample, len(sel)), random_state=42)
        o1, o2 = st.columns(2)
        color_opt = o1.selectbox("Colorier les points selon", ["(aucune)", "hour", "fare_amount", "trip_distance"])
        color_arg = None if color_opt == "(aucune)" else color_opt
        map_style = o2.selectbox("Fond de carte", ["carto-positron", "carto-darkmatter", "open-street-map",
                                                   "Sans fond de carte (nuage de points)"],
                                 help="Si le fond de carte ne s'affiche pas (réseau bloqué), choisis la dernière option.")

        st.header("🗺️ Carte interactive des points de départ")
        hover = {"trip_distance": ":.2f", "fare_amount": ":.2f", "hour": True}
        if map_style.startswith("Sans fond"):
            fig_m = px.scatter(
                smp, x="pickup_longitude", y="pickup_latitude", color=color_arg, opacity=0.6,
                hover_data=hover, height=560, color_continuous_scale="Sunsetdark",
                labels={"pickup_longitude": "Longitude", "pickup_latitude": "Latitude"},
            )
            fig_m.update_yaxes(scaleanchor="x", scaleratio=1)
            fig_m.update_layout(plot_bgcolor="#EEF2F7")
        else:
            fig_m = px.scatter_map(
                smp, lat="pickup_latitude", lon="pickup_longitude", color=color_arg,
                hover_data={**hover, "pickup_latitude": False, "pickup_longitude": False},
                zoom=10, opacity=0.6, map_style=map_style, height=560,
                color_continuous_scale="Sunsetdark",
            )
        if color_arg is None:
            fig_m.update_traces(marker=dict(color=ORANGE))
        fig_m.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        show_fig(fig_m)
        insight(
            "La grande majorité des départs se concentrent à <b>Manhattan</b>, surtout dans le centre (Midtown). "
            "Deux petits groupes isolés, à l'est de la ville, correspondent aux aéroports <b>JFK</b> et <b>LaGuardia</b>. "
            "Le taxi est utilisé surtout au cœur de la ville, avec les aéroports comme points de départ secondaires."
        )

        st.header("⏱️ Durée vs distance")
        fig_s = px.scatter(
            smp, x="trip_distance", y="duration_min", color=color_arg, opacity=0.5,
            hover_data={"fare_amount": ":.2f", "hour": True, "passenger_count": True},
            labels={"trip_distance": "Distance (miles)", "duration_min": "Durée (minutes)"},
            color_continuous_scale="Sunsetdark", height=480,
        )
        if color_arg is None:
            fig_s.update_traces(marker=dict(color=NAVY))
        fig_s.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        show_fig(fig_s)
        c_sel = sel[["trip_distance", "duration_min"]].corr().iloc[0, 1]
        insight(
            f"La durée augmente avec la distance (corrélation de <b>{c_sel:.2f}</b>). Mais pour une même distance, "
            "la durée varie beaucoup, surtout sur les trajets longs. Les trajets anormalement lents "
            "(points très au-dessus du nuage) correspondent probablement à des <b>embouteillages</b>."
        )
