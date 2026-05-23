import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OccuPredict · Dynamic Pricing",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    :root {
        --bg:        #0d0f14;
        --surface:   #141720;
        --surface2:  #1c2030;
        --border:    #2a2f45;
        --accent:    #5b8cff;
        --accent2:   #ff6b6b;
        --accent3:   #43e8b0;
        --accent4:   #f59e0b;
        --text:      #e8eaf0;
        --muted:     #6b7280;
        --radius:    12px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Syne', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    #MainMenu { display: none; }

    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
    }

    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent3));
    }
    .card-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 1rem;
    }

    .kpi-wrap {
        background: linear-gradient(135deg, #0d1a3a 0%, #0a1628 100%);
        border: 1px solid var(--accent);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        text-align: center;
        box-shadow: 0 0 40px rgba(91,140,255,0.15);
        position: relative;
        overflow: hidden;
    }
    .kpi-wrap::after {
        content: '';
        position: absolute;
        bottom: -30px; right: -30px;
        width: 120px; height: 120px;
        border-radius: 50%;
        background: rgba(91,140,255,0.07);
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'DM Mono', monospace;
        font-size: 4.5rem;
        font-weight: 500;
        line-height: 1;
        color: #fff;
    }
    .kpi-unit {
        font-size: 1.5rem;
        color: var(--muted);
        vertical-align: super;
        margin-left: 4px;
    }
    .kpi-bar-wrap {
        margin-top: 1.25rem;
        height: 8px;
        background: rgba(255,255,255,0.08);
        border-radius: 99px;
        overflow: hidden;
    }
    .kpi-bar-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.4s ease;
    }
    .kpi-status {
        margin-top: 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* ── Optimized Price card ── */
    .price-wrap {
        background: linear-gradient(135deg, #1a1200 0%, #120d00 100%);
        border: 1px solid var(--accent4);
        border-radius: 16px;
        padding: 1.75rem 2.5rem;
        text-align: center;
        box-shadow: 0 0 30px rgba(245,158,11,0.12);
        position: relative;
        overflow: hidden;
        margin-top: 1.25rem;
    }
    .price-wrap::after {
        content: '';
        position: absolute;
        bottom: -30px; right: -30px;
        width: 100px; height: 100px;
        border-radius: 50%;
        background: rgba(245,158,11,0.06);
    }
    .price-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent4);
        margin-bottom: 0.5rem;
    }
    .price-value {
        font-family: 'DM Mono', monospace;
        font-size: 3.5rem;
        font-weight: 500;
        line-height: 1;
        color: #fff;
    }
    .price-currency {
        font-size: 1.8rem;
        color: var(--accent4);
        margin-right: 4px;
    }
    .price-sub {
        margin-top: 0.6rem;
        font-size: 0.78rem;
        color: var(--muted);
        font-family: 'DM Mono', monospace;
    }

    .stSlider > div > div > div > div {
        background: var(--accent) !important;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }
    .stSlider label {
        color: var(--text) !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.85rem !important;
    }

    .stRadio label, .stSelectbox label {
        color: var(--text) !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.85rem !important;
    }
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: var(--text) !important;
    }
    div[role="radiogroup"] label {
        background: var(--surface2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        color: var(--text) !important;
        transition: border-color 0.2s;
    }
    div[role="radiogroup"] label:has(input:checked) {
        border-color: var(--accent) !important;
        background: rgba(91,140,255,0.12) !important;
        color: var(--accent) !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: var(--surface2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }

    .pill {
        display: inline-block;
        padding: 0.25rem 0.85rem;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .pill-live  { background: rgba(67,232,176,0.12); color: var(--accent3); border: 1px solid rgba(67,232,176,0.3); }
    .pill-err   { background: rgba(255,107,107,0.12); color: var(--accent2); border: 1px solid rgba(255,107,107,0.3); }
    .pill-idle  { background: rgba(107,114,128,0.12); color: var(--muted);  border: 1px solid rgba(107,114,128,0.3); }

    .section-header {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-header span { color: var(--accent); }

    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

    .stTextInput input {
        background: var(--surface2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
    }

    .num-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px; height: 22px;
        background: var(--accent);
        color: #fff;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 800;
        margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="padding: 1.5rem 0 1rem;">
        <div style="font-size:0.7rem;letter-spacing:0.25em;text-transform:uppercase;
                    color:#5b8cff;font-weight:700;margin-bottom:0.4rem;">
            Dynamic Pricing Engine
        </div>
        <div style="font-size:2.6rem;font-weight:800;line-height:1.1;color:#e8eaf0;">
            Occu<span style="color:#5b8cff;">Predict</span>
        </div>
        <div style="color:#6b7280;font-size:0.88rem;margin-top:0.4rem;">
            Tune every feature — live occupancy rate updates on every change.
        </div>
    </div>
    <hr/>
    """,
    unsafe_allow_html=True,
)

# ── Config row (toggle only) ──────────────────────────────────────────────────
backend_url = "http://localhost:8000/predict-occupancy"

_, toggle_col = st.columns([5, 1])
with toggle_col:
    auto_update = st.toggle("Live updates", value=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    # Group 1: Property
    st.markdown(
        '<div class="section-header"><span class="num-badge">1</span>Property Details</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Property ID</div>', unsafe_allow_html=True)
        property_id = st.text_input("🔑 Property ID", placeholder="e.g. PROP-00142", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Location & Amenities</div>', unsafe_allow_html=True)
        sl1, sl2 = st.columns(2)
        with sl1:
            location_score = st.slider("📍 Location Score", 0, 10, 5, step=1)
        with sl2:
            amenities_score = st.slider("🛎 Amenities Score", 0, 10, 5, step=1)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Classification</div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            season = st.radio(
                "🌦 Season",
                options=["Summer", "Winter", "Monsoon"],
                horizontal=True,
            )
        with r2:
            property_type = st.selectbox(
                "🏠 Property Type",
                options=["Entire house", "Private room", "Luxury suite"],
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Group 2: Events & Context
    st.markdown(
        '<div class="section-header" style="margin-top:0.5rem;"><span class="num-badge">2</span>Events & Context</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Flags</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            nearby_event_label = st.radio("🎪 Nearby Event", ["Yes", "No"], horizontal=True)
            nearby_event = 1 if nearby_event_label == "Yes" else 0
        with f2:
            holiday_label = st.radio("🏖 Holiday", ["Yes", "No"], horizontal=True)
            holiday = 1 if holiday_label == "Yes" else 0
        st.markdown("</div>", unsafe_allow_html=True)

    # Group 3: Market
    st.markdown(
        '<div class="section-header" style="margin-top:0.5rem;"><span class="num-badge">3</span>Market Signals</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Pricing & Demand</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            rating = st.slider("⭐ Rating", 0.0, 5.0, 3.5, step=0.1, format="%.1f")
            demand = st.slider("📈 Demand", 0.0, 1.0, 0.5, step=0.01, format="%.2f")
        with m2:
            competitor_price = st.slider("💰 Competitor Price (₹)", 0, 6000, 3000, step=50)
            market_trend = st.slider("📊 Market Trend", 1.0, 2.0, 1.5, step=0.01, format="%.2f")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><div class="card-title">Final Price</div>', unsafe_allow_html=True)
        final_price = st.slider("🏷 Final Price (₹)", 0, 6000, 2500, step=50)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Right column placeholders (must be declared before API call) ──────────────
with right:
    st.markdown(
        '<div class="section-header"><span class="num-badge" style="background:#43e8b0;color:#0d0f14;">◈</span>'
        'Live Prediction</div>',
        unsafe_allow_html=True,
    )

    kpi_placeholder    = st.empty()
    status_placeholder = st.empty()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Optimised pricing section
    st.markdown(
        '<div class="section-header"><span class="num-badge" style="background:#f59e0b;color:#0d0f14;">₹</span>'
        'Optimized Pricing</div>',
        unsafe_allow_html=True,
    )
    price_placeholder = st.empty()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Summary card
    st.markdown(
        '<div class="card"><div class="card-title">Current Input Summary</div>',
        unsafe_allow_html=True,
    )
    sum_left, sum_right = st.columns(2)
    summary_placeholder_l = sum_left.empty()
    summary_placeholder_r = sum_right.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Build payload ─────────────────────────────────────────────────────────────
payload = {
    "property_id":       property_id if property_id else None,
    "location_score":    location_score,
    "amenitites_score":  amenities_score,
    "season":            season.lower(),
    "property_type":     property_type,
    "nearby_event":      nearby_event,
    "holiday":           holiday,
    "rating":            round(rating, 2),
    "demand":            round(demand, 3),
    "competitor_price":  float(competitor_price),
    "market_trend":      round(market_trend, 3),
    "final_price":       float(final_price),
}

# ── Hit endpoint ──────────────────────────────────────────────────────────────
occupancy_rate   = None
optimized_price  = None
error_msg        = None

if auto_update:
    try:
        resp = requests.post(backend_url, json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        occupancy_rate  = float(data.get("occupancy_rate", 0))
        raw_price = data.get("optimized_price")
        if raw_price is not None:
            optimized_price = float(raw_price)
    except requests.exceptions.ConnectionError:
        error_msg = "Cannot reach backend — is it running?"
    except requests.exceptions.Timeout:
        error_msg = "Request timed out (>5 s)"
    except requests.exceptions.HTTPError:
        error_msg = f"HTTP {resp.status_code}: {resp.text[:120]}"
    except Exception as e:
        error_msg = str(e)[:150]

# ── Helpers ───────────────────────────────────────────────────────────────────
def occupancy_color(v):
    if v is None:  return "#6b7280"
    if v >= 0.75:  return "#43e8b0"
    if v >= 0.45:  return "#f59e0b"
    return "#ff6b6b"

def occupancy_label(v):
    if v is None:  return "—"
    if v >= 0.75:  return "🟢 High Demand"
    if v >= 0.45:  return "🟡 Moderate"
    return "🔴 Low Demand"

# ── Render Occupancy KPI ──────────────────────────────────────────────────────
if occupancy_rate is not None:
    pct = round(occupancy_rate * 100, 1)
    col = occupancy_color(occupancy_rate)
    lbl = occupancy_label(occupancy_rate)

    kpi_placeholder.markdown(
        f"""
        <div class="kpi-wrap">
            <div class="kpi-label">Predicted Occupancy Rate</div>
            <div class="kpi-value">
                {pct:.1f}<span class="kpi-unit">%</span>
            </div>
            <div class="kpi-bar-wrap">
                <div class="kpi-bar-fill"
                     style="width:{min(pct,100)}%;background:{col};"></div>
            </div>
            <div class="kpi-status" style="color:{col};">{lbl}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    status_placeholder.markdown(
        '<div style="margin-top:0.75rem;text-align:center;">'
        '<span class="pill pill-live">● Live</span></div>',
        unsafe_allow_html=True,
    )

elif error_msg:
    kpi_placeholder.markdown(
        f"""
        <div class="kpi-wrap" style="border-color:#ff6b6b;">
            <div class="kpi-label" style="color:#ff6b6b;">Connection Error</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.8rem;
                        color:#6b7280;margin-top:0.75rem;word-break:break-word;">
                {error_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    status_placeholder.markdown(
        '<div style="margin-top:0.75rem;text-align:center;">'
        '<span class="pill pill-err">✕ Error</span></div>',
        unsafe_allow_html=True,
    )

else:
    kpi_placeholder.markdown(
        """
        <div class="kpi-wrap">
            <div class="kpi-label">Predicted Occupancy Rate</div>
            <div class="kpi-value" style="color:#6b7280;">—</div>
            <div class="kpi-status" style="color:#6b7280;">Enable Live Updates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    status_placeholder.markdown(
        '<div style="margin-top:0.75rem;text-align:center;">'
        '<span class="pill pill-idle">◌ Paused</span></div>',
        unsafe_allow_html=True,
    )

# ── Render Optimized Price ────────────────────────────────────────────────────
if optimized_price is not None:
    vs_final = optimized_price - final_price
    direction = "▲" if vs_final >= 0 else "▼"
    diff_color = "#43e8b0" if vs_final >= 0 else "#ff6b6b"
    diff_text  = f"{direction} ₹{abs(vs_final):,.0f} vs final price"

    price_placeholder.markdown(
        f"""
        <div class="price-wrap">
            <div class="price-label">Optimized Price</div>
            <div class="price-value">
                <span class="price-currency">₹</span>{optimized_price:,.0f}
            </div>
            <div class="price-sub" style="color:{diff_color};margin-top:0.5rem;">
                {diff_text}
            </div>
            <div class="price-sub">per night · model recommendation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif error_msg:
    price_placeholder.markdown(
        """
        <div class="price-wrap" style="border-color:#2a2f45;">
            <div class="price-label" style="color:#6b7280;">Optimized Price</div>
            <div class="price-value" style="color:#6b7280;">—</div>
            <div class="price-sub">unavailable</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    price_placeholder.markdown(
        """
        <div class="price-wrap" style="border-color:#2a2f45;">
            <div class="price-label" style="color:#6b7280;">Optimized Price</div>
            <div class="price-value" style="color:#6b7280;">—</div>
            <div class="price-sub">enable live updates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Summary ───────────────────────────────────────────────────────────────────
summary_placeholder_l.markdown(
    f"""
    <div style="font-family:'DM Mono',monospace;font-size:0.78rem;
                line-height:2;color:#9ca3af;">
        <span style="color:#6b7280;">prop.id   </span>{property_id if property_id else "—"}<br/>
        <span style="color:#6b7280;">location  </span>{location_score}/10<br/>
        <span style="color:#6b7280;">amenities </span>{amenities_score}/10<br/>
        <span style="color:#6b7280;">season    </span>{season}<br/>
        <span style="color:#6b7280;">type      </span>{property_type[:12]}<br/>
        <span style="color:#6b7280;">event     </span>{nearby_event_label}<br/>
        <span style="color:#6b7280;">holiday   </span>{holiday_label}
    </div>
    """,
    unsafe_allow_html=True,
)
summary_placeholder_r.markdown(
    f"""
    <div style="font-family:'DM Mono',monospace;font-size:0.78rem;
                line-height:2;color:#9ca3af;">
        <span style="color:#6b7280;">rating     </span>{rating:.1f}/5<br/>
        <span style="color:#6b7280;">demand     </span>{demand:.2f}<br/>
        <span style="color:#6b7280;">comp.price </span>₹{competitor_price}<br/>
        <span style="color:#6b7280;">trend      </span>{market_trend:.2f}<br/>
        <span style="color:#6b7280;">final.price</span>₹{final_price}
    </div>
    """,
    unsafe_allow_html=True,
)