import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Video Game Sales Dashboard", page_icon="🎮", layout="wide")

BG        = "#0D1B2A"
CARD_BG   = "#1E3A52"
GRID_CLR  = "#203656"
TEXT_CLR  = "#FFFFFF"
ACCENT    = "#4488DD"
DONUT_COLORS = ["#4488DD","#03F869","#AA55CC","#ebbb6a"]

st.markdown(f"""
<style>
  .stApp {{ background-color: {BG}; }}
  section[data-testid="stSidebar"] {{ background-color: {CARD_BG}; }}
  h1,h2,h3,h4,p {{ color: {TEXT_CLR} !important; }}
  .donut-card {{ background:{CARD_BG};border:1px solid {GRID_CLR};border-radius:8px;padding:10px;text-align:center; }}
  .donut-label {{ color:{ACCENT};font-size:12px;font-weight:600; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    sales = pd.read_csv("vg_sales.csv")
    genres = pd.read_csv("vg_genres.csv")
    publishers = pd.read_csv("vg_publishers.csv")

    if 'Genre_ID' in sales.columns and 'Genre_ID' in genres.columns:
        sales = sales.merge(genres, on='Genre_ID', how='left')
    if 'Publisher_ID' in sales.columns and 'Publisher_ID' in publishers.columns:
        sales = sales.merge(publishers, on='Publisher_ID', how='left')

    sales['Publish_Year'] = pd.to_datetime(sales['Publish_Year'], errors='coerce').dt.year
    sales = sales.dropna(subset=['NA_Sales'])
    sales['Global_Sales'] = (sales['NA_Sales'].fillna(0) + sales['EU_Sales'].fillna(0) +
                              sales['JP_Sales'].fillna(0) + sales['Other_Sales'].fillna(0))

    gcol = [c for c in sales.columns if 'genre' in c.lower() and c != 'Genre_ID']
    pcol = [c for c in sales.columns if 'publisher' in c.lower() and c != 'Publisher_ID']
    sales['Genre']     = sales[gcol[0]] if gcol else 'Unknown'
    sales['Publisher'] = sales[pcol[0]] if pcol else 'Unknown'

    sales['Month']    = pd.to_datetime(sales['Publish_Year'].astype(str) + '-01-01', errors='coerce').dt.month_name()
    sales['day_name'] = 'N/A'
    return sales

df = load_data()

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=CARD_BG,
    font=dict(color=TEXT_CLR, family="Segoe UI"),
    margin=dict(l=10,r=10,t=30,b=10)
)

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h3 style='color:{ACCENT}'>🔽 Filters</h3>", unsafe_allow_html=True)
    genre_opts = sorted(df['Genre'].dropna().unique())
    sel_genre  = st.selectbox("Genre", ["All"] + genre_opts)

    yr_min, yr_max = int(df['Publish_Year'].min()), int(df['Publish_Year'].max())
    sel_years = st.slider("Year Range", yr_min, yr_max, (yr_min, yr_max))

    game_opts = sorted(df['Game_Name'].dropna().unique())
    sel_games = st.multiselect("Game Name", game_opts, default=[])
    st.markdown("---")
    st.markdown(f"<small style='color:{TEXT_CLR}'>👩‍💻 Sneha Shree M U</small>", unsafe_allow_html=True)

# ── Filter ─────────────────────────────────────────────────────────────────────
f = df[df['Publish_Year'].between(*sel_years)]
if sel_genre != "All":
    f = f[f['Genre'] == sel_genre]
if sel_games:
    f = f[f['Game_Name'].isin(sel_games)]

# ── Title ──────────────────────────────────────────────────────────────────────
st.markdown(f"<h2 style='color:{TEXT_CLR};text-align:center'>🎮 Global Video Game Sales Dashboard</h2>", unsafe_allow_html=True)

# ── 4 Donut Charts (matching Power BI exactly) ─────────────────────────────────
st.markdown(f"<h4 style='color:{TEXT_CLR}'>Regional Sales Breakdown</h4>", unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4)

for col, label, region_col, center_color in [
    (d1, "EU Sales",    "EU_Sales",    "#4488DD"),
    (d2, "NA Sales",    "NA_Sales",    "#03F869"),
    (d3, "JP Sales",    "JP_Sales",    "#AA55CC"),
    (d4, "Other Sales", "Other_Sales", "#ebbb6a"),
]:
    total = f[region_col].sum()
    other = f['Global_Sales'].sum() - total
    donut_df = pd.DataFrame({
        'Region': [label, 'Others'],
        'Sales': [total, max(other, 0)]
    })
    fig = px.pie(donut_df, names='Region', values='Sales', hole=0.6,
                 color_discrete_sequence=[center_color, GRID_CLR])
    fig.update_traces(textposition='inside', textinfo='percent',
                      textfont=dict(color=TEXT_CLR, size=11))
    fig.update_layout(**LAYOUT, height=200, showlegend=False,
                      annotations=[dict(text=f"<b>{total:.1f}M</b>",
                                        x=0.5, y=0.5, font_size=13,
                                        font_color=TEXT_CLR, showarrow=False)])
    col.markdown(f"<div class='donut-card'><div class='donut-label'>{label}</div>", unsafe_allow_html=True)
    col.plotly_chart(fig, use_container_width=True)
    col.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 2: Column Chart (Top Games) + Decomposition Tree ──────────────────────
c1, c2 = st.columns([1.6, 1])

with c1:
    st.markdown(f"<h4 style='color:{TEXT_CLR}'>Top Games by Total Sales (Column Chart)</h4>", unsafe_allow_html=True)
    top_games = f.groupby('Game_Name')['Global_Sales'].sum().nlargest(10).reset_index()
    top_games.columns = ['Game_Name','Total_Sales']
    fig = go.Figure(go.Bar(
        x=top_games['Game_Name'], y=top_games['Total_Sales'],
        marker_color=ACCENT,
        text=top_games['Total_Sales'].apply(lambda x: f"{x:.1f}M"),
        textposition='outside', textfont=dict(color=TEXT_CLR, size=11)
    ))
    fig.update_layout(**LAYOUT, height=380,
                      xaxis=dict(color=TEXT_CLR, tickangle=30, gridcolor=GRID_CLR),
                      yaxis=dict(color=TEXT_CLR, gridcolor=GRID_CLR))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown(f"<h4 style='color:{TEXT_CLR}'>Global Sales by Year (Decomposition)</h4>", unsafe_allow_html=True)
    yr_df = f.groupby('Publish_Year')['Global_Sales'].sum().reset_index().sort_values('Publish_Year')
    yr_df.columns = ['Year','Global_Sales']
    fig = go.Figure(go.Bar(
        x=yr_df['Year'], y=yr_df['Global_Sales'],
        marker_color=ACCENT,
        text=yr_df['Global_Sales'].apply(lambda x: f"{x:.0f}M"),
        textposition='outside', textfont=dict(color=TEXT_CLR, size=9)
    ))
    fig.update_layout(**LAYOUT, height=380,
                      xaxis=dict(color=TEXT_CLR, tickangle=45, gridcolor=GRID_CLR),
                      yaxis=dict(color=TEXT_CLR, gridcolor=GRID_CLR),
                      title=dict(text="Total Global Sales by Year", font=dict(color=TEXT_CLR, size=12)))
    st.plotly_chart(fig, use_container_width=True)

st.caption("Built by Sneha Shree M U | Data Analyst & Data Scientist | Bangalore")
