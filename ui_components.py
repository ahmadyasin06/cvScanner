"""
ui_components.py
Minimal, self-contained UI building blocks: skill chips, a lightweight
score badge, candidate cards, and empty states.
"""

import streamlit as st
import json


def safe_jason_list(data):
  """Ensures the data is safely converted to a list, handling None, JSON, and strings."""
  if data is None:
    return []

  # Agar data pehle hi list hai
  if isinstance(data, list):
    return data

  # Agar data string hai
  if isinstance(data, str):
    data = data.strip()
    if not data or data.lower() == 'none':
      return []

    import json

    # 1. Try standard JSON parsing
    try:
      parsed = json.loads(data)
      if isinstance(parsed, list):
        return parsed
    except:
      pass

    # 2. Try python literal evaluation (agar single quotes wala format ho like ['qweq'])
    try:
      import ast

      parsed = ast.literal_eval(data)
      if isinstance(parsed, list):
        return parsed
    except:
      pass

    # 3. Agar simple text ho toh usay list mein dal dein
    return [data.strip("'\"")]

  return []

# ---------- Style helpers ----------

def score_color(score: int) -> str:
    score = int(score) if score is not None else 0
    if score >= 75:
        return "#22c55e"   # green
    elif score >= 50:
        return "#eab308"   # yellow
    else:
        return "#ef4444"   # red


def recommendation_badge_style(recommendation: str):
    styles = {
        "Strongly Recommended": ("#22c55e", "#ecfdf5"),
        "Consider": ("#eab308", "#fefce8"),
        "Not Recommended": ("#ef4444", "#fef2f2"),
    }
    return styles.get(recommendation, ("#6b7280", "#f3f4f6"))


# ---------- Inject global CSS ----------

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* ================= MAIN CONTENT ================= */
        .main { 
            background-color: #0F0F1A; 
        }

        .candidate-card {
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.07);
            border-left: 4px solid var(--score-color, #6b7280);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .candidate-name {
            font-size: 17px;
            font-weight: 700;
            color: #111827;
        }

        .score-circle {
            width: 46px;
            height: 46px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 15px;
            flex-shrink: 0;
        }

        .meta-text {
            color: #000000;
            font-size: 13px;
            margin: 6px 0 12px 0;
        }

        .section-label {
            font-size: 11px;
            font-weight: 700;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: .04em;
            margin: 10px 0 4px 0;
        }

        .explanation-text {
            color: #000000;
            font-weight: 200;
            font-size: 15px;
            margin-top: 10px;
            line-height: 1.5;
        }

        .skill-chip {
            display: inline-block;
            padding: 3px 12px;
            border-radius: 999px;
            font-size: 12.5px;
            font-weight: 600;
            margin: 3px 4px 3px 0;
        }

        .skill-chip-matched {
            background-color: #ecfdf5;
            color: #16a34a;
            border: 1px solid #86efac;
        }

        .skill-chip-missing {
            background-color: #fef2f2;
            color: #dc2626;
            border: 1px solid #fca5a5;
        }

        .skill-chip-neutral {
            background-color: #eff6ff;
            color: #2563eb;
            border: 1px solid #93c5fd;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 12px;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        }

        /* ================= SIDEBAR BASE STYLES ================= */
        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #1f2937 !important;
            transition: transform 0.3s ease-in-out !important;
        }

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] * {
            color: #f3f4f6 !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background-color: #1f2937 !important;
            color: #f3f4f6 !important;
            border: 1px solid #374151 !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            background-color: #374151 !important;
            color: #ffffff !important;
            border-color: #4b5563 !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background-color: #FF4B4B !important;
            color: #ffffff !important;
            box-shadow: 0 4px 10px rgba(255, 255, 255, 0.25) !important;
        }

        /* Hide Input Instructions */
        div[data-testid="stInputInstruction"],
        [data-testid="stInputInstruction"] small,
        .st-emotion-cache-12w0q3e, 
        .st-emotion-cache-1g88y40 {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        div[data-baseweb="base-input"] + div {
            display: none !important;
        }

        /* ================= DESKTOP VIEW (> 768px) ================= */
        @media (min-width: 769px) {
            div[data-testid="stAppViewContainer"] > div:first-child {
                padding-top: 0rem !important;
            }

            div[data-testid="stMainBlockContainer"],
            div[data-testid="block-container"],
            .block-container {
                padding-top: 2.5rem !important;
            }

            section[data-testid="stSidebar"] .stButton > button {
                width: 100% !important;
            }

            section[data-testid="stSidebar"] {
                min-width: 21rem !important;
                max-width: 21rem !important;
                width: 21rem !important;
            }
        }

        /* ================= MOBILE VIEW (<= 768px) ================= */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] > div:first-child {
                padding: 16px 12px !important;
            }

            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                display: flex !important;
                flex-direction: column !important;
                gap: 12px !important;
                width: 100% !important;
            }

            section[data-testid="stSidebar"] .stButton > button {
                width: 100% !important;
                padding: 8px 12px !important;
                font-size: 14px !important;
            }

            div[data-testid="stMainBlockContainer"],
            div[data-testid="block-container"],
            .block-container {
                padding-top: 2rem !important;
                padding-left: 12px !important;
                padding-right: 12px !important;
            }

            .candidate-card {
                padding: 14px 16px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- Skill chips ----------

def _skill_chips_html(skills, kind="neutral") -> str:
  """Build the chip HTML as a string (used inside a single card block)."""
  skills = safe_jason_list(skills)

  if not skills:
    return '<span style="color:#9ca3af; font-size:13px;">None</span>'

  css_class = f"skill-chip-{kind}"
  return "".join(
      f'<span class="skill-chip {css_class}">{s}</span>' for s in skills
  )


def render_skill_tags(skills, kind="neutral"):
    """Standalone version for use outside a single-block card (e.g. History page)."""
    st.markdown(_skill_chips_html(skills, kind), unsafe_allow_html=True)


# ---------- Score badge ----------

def render_score_gauge(score: int, key: str = None):
    """Lightweight standalone score circle (no charting library needed)."""
    score = int(score) if score is not None else 0 
    color = score_color(score)
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
            <div class="score-circle" style="width:72px;height:72px;font-size:22px;
                background:{color}1a; color:{color}; border:2px solid {color};">
                {score}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Candidate card ----------

def render_candidate_card(result: dict, job_required_skills=None, is_best_match=False, key_prefix=""):
    """Renders the full candidate card as a single HTML block."""
    score = int(result.get("match_score", 0))
    color = score_color(score)
    badge_color, badge_bg = recommendation_badge_style(result.get("recommendation", ""))

    matched_skills = safe_jason_list(result.get("matched_skills", []))
    missing_skills = safe_jason_list(result.get("missing_skills", []))

    best_match_tag = (
        '<span style="color:#f59e0b; font-weight:700; font-size:12px; margin-left:8px;">🏆 Best Match</span>'
        if is_best_match else ""
    )

    card_html = f"""
    <div class="candidate-card" style="--score-color:{color};">
        <div class="card-top">
            <span class="candidate-name">{result.get('candidate_name', 'Unknown Candidate')}{best_match_tag}</span>
            <div class="score-circle" style="background:{color}1a; color:{color}; border:2px solid {color};">{score}</div>
        </div>
        <div class="meta-text">
            <span class="badge" style="background-color:{badge_bg}; color:{badge_color};">{result.get('recommendation', 'N/A')}</span>
            &nbsp;&nbsp;{result.get('total_experience_years', 'N/A')} yrs exp &nbsp;•&nbsp; {result.get('education', 'N/A')}
        </div>
            <div class="meta-text" style="margin-top:-6px;">
    📧      {result.get('email', 'Not found')} &nbsp;•&nbsp; 📱 {result.get('phone', 'Not found')}
        </div>
        <div class="section-label">Matched Skills</div>
        <div>{_skill_chips_html(matched_skills, 'matched')}</div>
        <div class="section-label">Missing Skills</div>
        <div>{_skill_chips_html(missing_skills, 'missing')}</div>
        <div class="explanation-text">{result.get('explanation', '')}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# ---------- Empty states ----------

def render_empty_state(icon: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="empty-state">
            <div style="font-size: 44px;">{icon}</div>
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Skill input preview (upload page) ----------

def render_skill_input_preview(raw_skills_text: str):
    skills = [s.strip() for s in raw_skills_text.split(",") if s.strip()]
    if skills:
        render_skill_tags(skills, kind="neutral")
    return skills


def safe_json_list(value):
    """Parse a JSON-encoded list stored in SQLite back into a Python list."""
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, json.JSONDecodeError):
        return []
