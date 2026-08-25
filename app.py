import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sports Global Sales Dashboard", page_icon="⚡", layout="wide")

# ── Exact Power BI colors from pbix ───────────────────────────────────────────
BG       = "#0D1B2A"   # page background dark navy
CARD_BG  = "#1E3A52"   # card background
LINE_CLR = "#203656"   # borders
TEXT_CLR = "#FFFFFF"   # white text
MUTED    = "#73DBE1"   # cyan muted
EU_CLR   = "#73DBE1"   # EU donut cyan
NA_CLR   = "#4488DD"   # NA donut blue
JP_CLR   = "#CC44CC"   # JP donut purple
OT_CLR   = "#ebbb6a"   # Other donut amber
BAR_CLR  = "#4488DD"   # column chart bar color
DECOMP_COLORS = ["#03F869","#ebbb6a","#fae9a0","#dd0f31","#AA55CC"]

st.markdown(f"""
<style>
  .stApp, [data-testid="stAppViewContainer"],
  [data-testid="block-container"] {{
    background-color: {BG} !important;
  }}
  section[data-testid="stSidebar"] {{ display:none !important; }}
  h1,h2,h3,h4,p,span,label,div {{ color:{TEXT_CLR} !important; }}
  .title-bar {{
    background:{BG};
    border-bottom: 1px solid {LINE_CLR};
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
  }}
  .donut-card {{
    background:{CARD_BG};
    border-radius:10px;
    padding:12px 8px 6px 8px;
    text-align:center;
    border:1px solid {LINE_CLR};
  }}
  .donut-label {{
    font-size:11px;
    font-weight:600;
    margin-bottom:4px;
    text-transform:uppercase;
    letter-spacing:0.5px;
  }}
  .donut-pct {{
    font-size:26px;
    font-weight:700;
    margin-top:-10px;
  }}
  .game-btn {{
    background:{CARD_BG};
    border:2px solid {LINE_CLR};
    border-radius:30px;
    padding:10px 16px;
    font-size:13px;
    font-weight:600;
    text-align:center;
    margin-bottom:6px;
  }}
  .chart-card {{
    background:{CARD_BG};
    border:1px solid {LINE_CLR};
    border-radius:8px;
    padding:12px;
    margin-bottom:10px;
  }}
  .stButton>button {{
    background:{CARD_BG};
    color:{TEXT_CLR};
    border:1px solid {LINE_CLR};
    border-radius:6px;
    width:100%;
  }}
  [data-baseweb="select"]>div {{
    background:{CARD_BG} !important;
    border-color:{LINE_CLR} !important;
    color:{TEXT_CLR} !important;
  }}
  [data-baseweb="select"] span {{ color:{TEXT_CLR} !important; }}
  .stSlider [data-testid="stMarkdownContainer"] p {{ color:{TEXT_CLR} !important; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    sales  = pd.read_csv("vg_sales.csv")
    genres = pd.read_csv("vg_genres.csv")
    pubs   = pd.read_csv("vg_publishers.csv")
    df = sales.merge(genres, on='Genre_ID', how='left')
    df = df.merge(pubs, on='Publisher_ID', how='left')
    df['Year'] = pd.to_datetime(df['Publish_Year'], errors='coerce').dt.year
    df = df.dropna(subset=['NA_Sales'])
    df['NA_Sales']    = df['NA_Sales'].fillna(0)
    df['EU_Sales']    = df['EU_Sales'].fillna(0)
    df['JP_Sales']    = df['JP_Sales'].fillna(0)
    df['Other_Sales'] = df['Other_Sales'].fillna(0)
    df['total_of_all_sales'] = df['NA_Sales'] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales']
    df['Total_Global_Sales'] = df['total_of_all_sales']
    # Day name for decomposition tree (derived from year/date)
    df['day_name'] = pd.to_datetime(df['Publish_Year'], errors='coerce').dt.day_name().fillna('(Blank)')
    df['Month']    = pd.to_datetime(df['Publish_Year'], errors='coerce').dt.strftime('%b').fillna('(Blank)')
    return df

df = load_data()

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=CARD_BG,
    font=dict(color=TEXT_CLR, family="Segoe UI", size=11),
    margin=dict(l=8, r=8, t=28, b=8),
)

# ── Top title bar ──────────────────────────────────────────────────────────────
t1, t2 = st.columns([3, 2])
with t1:
    st.markdown(f"<h3 style='color:{TEXT_CLR};margin:0;'>⚡ Sports Global Sales Dashboard</h3>",
                unsafe_allow_html=True)
with t2:
    # Flag buttons matching Power BI top right
    fb1,fb2,fb3,fb4,fb5 = st.columns(5)
    fb1.markdown(f"<div style='background:{CARD_BG};border-radius:6px;padding:6px;text-align:center;border:1px solid {LINE_CLR};'>🧹</div>", unsafe_allow_html=True)
    fb2.markdown(f"<div style='background:{CARD_BG};border-radius:6px;padding:6px;text-align:center;border:1px solid {LINE_CLR};'>🇪🇺</div>", unsafe_allow_html=True)
    fb3.markdown(f"<div style='background:{CARD_BG};border-radius:6px;padding:6px;text-align:center;border:1px solid {LINE_CLR};'>🇯🇵</div>", unsafe_allow_html=True)
    fb4.markdown(f"<div style='background:{CARD_BG};border-radius:6px;padding:6px;text-align:center;border:1px solid {LINE_CLR};'>🇳🇦</div>", unsafe_allow_html=True)
    fb5.markdown(f"<div style='background:{CARD_BG};border-radius:6px;padding:6px;text-align:center;border:1px solid {LINE_CLR};'>❓</div>", unsafe_allow_html=True)

st.markdown(f"<hr style='border-color:{LINE_CLR};margin:6px 0 10px 0;'>", unsafe_allow_html=True)

# ── Main layout: Left filters | Right content ──────────────────────────────────
left, right = st.columns([1, 2.8])

with left:
    # Clear all slicers
    if st.button("Clear all slicers", use_container_width=True):
        for k in ['genre_sel','year_range','game_sel']:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Genre slicer dropdown
    st.markdown(f"<p style='color:{TEXT_CLR};font-size:12px;font-weight:600;margin-bottom:2px;'>Genre</p>",
                unsafe_allow_html=True)
    genre_opts = ['All'] + sorted(df['Genre'].dropna().unique().tolist())
    sel_genre  = st.selectbox("", genre_opts,
                               index=0, label_visibility="collapsed", key="genre_sel")

    st.markdown("<br>", unsafe_allow_html=True)

    # Year range slider
    st.markdown(f"<p style='color:{TEXT_CLR};font-size:12px;font-weight:600;margin-bottom:2px;'>Year</p>",
                unsafe_allow_html=True)
    years = sorted(df['Year'].dropna().unique().astype(int).tolist())
    yr_min, yr_max = min(years), max(years)
    if 'year_range' not in st.session_state:
        st.session_state.year_range = (yr_min, yr_max)
    y1c, y2c = st.columns(2)
    with y1c:
        st.markdown(f"<div style='background:{CARD_BG};border:1px solid {LINE_CLR};border-radius:4px;padding:4px 8px;font-size:12px;'>{yr_min}</div>", unsafe_allow_html=True)
    with y2c:
        st.markdown(f"<div style='background:{CARD_BG};border:1px solid {LINE_CLR};border-radius:4px;padding:4px 8px;font-size:12px;'>{yr_max}</div>", unsafe_allow_html=True)
    sel_years = st.slider("", yr_min, yr_max, (yr_min, yr_max),
                          label_visibility="collapsed", key="year_range")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Decomposition Tree (Total_Global_Sales by day_name → Month → Year) ────
    st.markdown(f"<p style='color:{TEXT_CLR};font-size:12px;font-weight:600;margin-bottom:6px;'>Total_Global_Sales_Based_On_Period</p>",
                unsafe_allow_html=True)

    # Apply filters for decomp
    fd = df.copy()
    if sel_genre != 'All':
        fd = fd[fd['Genre'] == sel_genre]
    fd = fd[fd['Year'].between(*sel_years)]

    # Decomposition by day_name
    decomp_day = fd.groupby('day_name')['Total_Global_Sales'].sum().reset_index()
    decomp_day = decomp_day.sort_values('Total_Global_Sales', ascending=True)

    fig_decomp = go.Figure()
    colors_cycle = DECOMP_COLORS
    for i, row in decomp_day.iterrows():
        fig_decomp.add_trace(go.Bar(
            x=[row['Total_Global_Sales']],
            y=[row['day_name']],
            orientation='h',
            marker_color=colors_cycle[i % len(colors_cycle)],
            text=[f"{row['Total_Global_Sales']:.0f}"],
            textposition='outside',
            textfont=dict(color=TEXT_CLR, size=9),
            showlegend=False,
            name=row['day_name']
        ))
    fig_decomp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG,
        font=dict(color=TEXT_CLR, size=9),
        margin=dict(l=0,r=4,t=0,b=0),
        height=320,
        barmode='stack',
        xaxis=dict(showgrid=False, color=TEXT_CLR, showticklabels=False),
        yaxis=dict(color=TEXT_CLR, showgrid=False),
        showlegend=False
    )
    st.plotly_chart(fig_decomp, use_container_width=True)

    # Month breakdown below
    decomp_month = fd.groupby('Month')['Total_Global_Sales'].sum().reset_index()
    decomp_month = decomp_month.sort_values('Total_Global_Sales', ascending=False)
    fig_month = go.Figure()
    for i, row in decomp_month.iterrows():
        fig_month.add_trace(go.Bar(
            x=[row['Total_Global_Sales']],
            y=[row['Month']],
            orientation='h',
            marker_color="#03F869",
            text=[f"{row['Total_Global_Sales']:.0f}"],
            textposition='outside',
            textfont=dict(color=TEXT_CLR, size=9),
            showlegend=False,
        ))
    fig_month.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG,
        font=dict(color=TEXT_CLR, size=9),
        margin=dict(l=0,r=4,t=0,b=0),
        height=280,
        xaxis=dict(showgrid=False, color=TEXT_CLR, showticklabels=False),
        yaxis=dict(color=TEXT_CLR, showgrid=False),
        showlegend=False
    )
    st.plotly_chart(fig_month, use_container_width=True)

with right:
    # Apply all filters
    f = df.copy()
    if sel_genre != 'All':
        f = f[f['Genre'] == sel_genre]
    f = f[f['Year'].between(*sel_years)]

    total = f['total_of_all_sales'].sum()
    eu_pct  = (f['EU_Sales'].sum()    / total * 100) if total else 0
    na_pct  = (f['NA_Sales'].sum()    / total * 100) if total else 0
    jp_pct  = (f['JP_Sales'].sum()    / total * 100) if total else 0
    oth_pct = (f['Other_Sales'].sum() / total * 100) if total else 0

    # ── 4 Donut KPI cards ─────────────────────────────────────────────────────
    d1, d2, d3, d4 = st.columns(4)

    for col, label, pct, clr, flag in [
        (d1, "Total_EU_Sales",    eu_pct,  EU_CLR, "🇪🇺"),
        (d2, "Total_NA_Sales",    na_pct,  NA_CLR, "🇺🇸"),
        (d3, "Total_JP_Sales",    jp_pct,  JP_CLR, "🇯🇵"),
        (d4, "Total_Other_Sales", oth_pct, OT_CLR, "🌍"),
    ]:
        remainder = 100 - pct
        fig_d = go.Figure(go.Pie(
            values=[pct, remainder],
            hole=0.72,
            marker_colors=[clr, LINE_CLR],
            direction='clockwise',
            sort=False,
            showlegend=False,
            textinfo='none',
        ))
        fig_d.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0),
            height=160,
            annotations=[dict(
                text=f"<b>{pct:.2f}%</b>",
                x=0.5, y=0.5,
                font=dict(size=16, color=clr),
                showarrow=False
            )]
        )
        col.markdown(f"<div class='donut-card'><div class='donut-label' style='color:{clr};'>{label}</div>", unsafe_allow_html=True)
        col.plotly_chart(fig_d, use_container_width=True)
        col.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top 4 game buttons (matching Power BI bookmark buttons) ───────────────
    top4_games = f.groupby('Game_Name')['total_of_all_sales'].sum().nlargest(4).index.tolist()
    btn_colors = [
        ("#73DBE1","#1E4A5A"),  # cyan
        ("#CC44CC","#3A1A4A"),  # purple
        ("#8B7355","#3A2A1A"),  # brown
        ("#4A6AAA","#1A2A4A"),  # blue
    ]
    gb1,gb2,gb3,gb4 = st.columns(4)
    for col, game, (border, bg) in zip([gb1,gb2,gb3,gb4], top4_games, btn_colors):
        col.markdown(f"""<div style='background:{bg};border:2px solid {border};
            border-radius:30px;padding:10px 8px;text-align:center;
            font-size:12px;font-weight:600;color:{TEXT_CLR};margin-bottom:8px;'>
            {game}</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Column Chart: Sum of total_of_all_sales by Game_Name ──────────────────
    st.markdown(f"<div class='chart-card'>", unsafe_allow_html=True)
    top_games = f.groupby('Game_Name')['total_of_all_sales'].sum().nlargest(10).reset_index()
    top_games = top_games.sort_values('total_of_all_sales', ascending=False)

    fig_bar = go.Figure(go.Bar(
        x=top_games['Game_Name'],
        y=top_games['total_of_all_sales'],
        marker_color=BAR_CLR,
        marker_line_color=LINE_CLR,
        marker_line_width=1,
        text=top_games['total_of_all_sales'].apply(lambda x: f"{x/1000:.3f}K"),
        textposition='outside',
        textfont=dict(color=TEXT_CLR, size=10),
    ))
    fig_bar.update_layout(**LAYOUT, height=340,
        title=dict(text="Sum of total_of_all_sales by Game_Name",
                   font=dict(color=TEXT_CLR, size=12), x=0.5),
        xaxis=dict(title='Game_Name', color=TEXT_CLR,
                   gridcolor=LINE_CLR, showgrid=False,
                   tickangle=15),
        yaxis=dict(title='Sum of total_of_all_sales', color=TEXT_CLR,
                   gridcolor=LINE_CLR,
                   tickformat=',.2s'))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Built by Sneha Shree M U | Data Analyst & Data Scientist | Bangalore")
