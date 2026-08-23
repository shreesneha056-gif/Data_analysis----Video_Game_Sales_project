import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Video Game Sales Dashboard", page_icon="🎮", layout="wide")

st.markdown("""<style>
.title-bar{background:linear-gradient(90deg,#1a1a2e,#16213e,#0f3460);padding:18px;border-radius:10px;margin-bottom:20px;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("vg_sales.csv")
    genres = pd.read_csv("vg_genres.csv")
    publishers = pd.read_csv("vg_publishers.csv")

    # Merge
    if 'Genre_ID' in df.columns and 'Genre_ID' in genres.columns:
        df = df.merge(genres, on='Genre_ID', how='left')
    if 'Publisher_ID' in df.columns and 'Publisher_ID' in publishers.columns:
        df = df.merge(publishers, on='Publisher_ID', how='left')

    df['Publish_Year'] = pd.to_datetime(df['Publish_Year'], errors='coerce').dt.year
    df = df.dropna(subset=['NA_Sales'])
    df['Global_Sales'] = df['NA_Sales'] + df['EU_Sales'].fillna(0) + df['JP_Sales'].fillna(0) + df['Other_Sales'].fillna(0)

    genre_col   = [c for c in df.columns if 'genre' in c.lower() and c != 'Genre_ID']
    pub_col     = [c for c in df.columns if 'publisher' in c.lower() and c != 'Publisher_ID']
    df['Genre']     = df[genre_col[0]] if genre_col else 'Unknown'
    df['Publisher'] = df[pub_col[0]]   if pub_col   else 'Unknown'
    return df

df = load_data()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="title-bar"><h2 style="color:white;margin:0;">🎮 Global Video Game Sales Dashboard</h2><p style="color:#aab4be;margin:0;">Publisher & Genre Performance Analytics (1980–Present) — Sneha Shree M U</p></div>', unsafe_allow_html=True)

# ── Sidebar Filters ─────────────────────────────────────────────────────────────
st.sidebar.title("🔽 Filters")

years = sorted(df['Publish_Year'].dropna().unique().astype(int))
sel_years = st.sidebar.select_slider("📅 Year Range", options=years, value=(int(min(years)), int(max(years))))

genres = sorted(df['Genre'].dropna().unique())
sel_genre = st.sidebar.multiselect("🎯 Genre", genres, default=genres)

top_pubs = df.groupby('Publisher')['Global_Sales'].sum().nlargest(30).index.tolist()
all_pubs = ['All Publishers'] + top_pubs
sel_pub = st.sidebar.selectbox("🏢 Publisher (Top 30)", all_pubs)

regions_map = {'NA_Sales':'North America','EU_Sales':'Europe','JP_Sales':'Japan','Other_Sales':'Other'}
sel_region = st.sidebar.selectbox("🌍 Sales Region (for charts)", list(regions_map.values()))
region_col = {v:k for k,v in regions_map.items()}[sel_region]

st.sidebar.markdown("---")
st.sidebar.markdown("**👩‍💻 Built by Sneha Shree M U**")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/sneha-shree-mu/) | [GitHub](https://github.com/shreesneha056-gif)")

# ── Filter ─────────────────────────────────────────────────────────────────────
filtered = df[
    df['Publish_Year'].between(*sel_years) &
    df['Genre'].isin(sel_genre)
]
if sel_pub != 'All Publishers':
    filtered = filtered[filtered['Publisher'] == sel_pub]

# ── KPIs ───────────────────────────────────────────────────────────────────────
st.markdown("### 📌 Key Performance Indicators")
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("🎮 Total Games",         f"{len(filtered):,}")
k2.metric("🌐 Global Sales (M)",    f"{filtered['Global_Sales'].sum():.1f}M")
k3.metric("🇺🇸 NA Sales (M)",       f"{filtered['NA_Sales'].sum():.1f}M")
k4.metric("🇪🇺 EU Sales (M)",       f"{filtered['EU_Sales'].sum():.1f}M")
k5.metric("🇯🇵 JP Sales (M)",       f"{filtered['JP_Sales'].sum():.1f}M")

st.markdown("---")

# ── Row 1 ──────────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 🎯 Sales by Genre")
    genre_df = filtered.groupby('Genre')['Global_Sales'].sum().reset_index().sort_values('Global_Sales', ascending=True).tail(12)
    fig = px.bar(genre_df, x='Global_Sales', y='Genre', orientation='h',
                 color='Global_Sales', color_continuous_scale='Purples',
                 text=genre_df['Global_Sales'].apply(lambda x: f"{x:.1f}M"))
    fig.update_traces(textposition='outside')
    fig.update_layout(height=380, showlegend=False, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### 🌍 Regional Sales Breakdown")
    reg_totals = {
        'North America': filtered['NA_Sales'].sum(),
        'Europe':        filtered['EU_Sales'].sum(),
        'Japan':         filtered['JP_Sales'].sum(),
        'Other':         filtered['Other_Sales'].sum()
    }
    reg_df = pd.DataFrame(list(reg_totals.items()), columns=['Region','Sales'])
    fig = px.pie(reg_df, names='Region', values='Sales', hole=0.45,
                 color_discrete_sequence=['#3498db','#2ecc71','#e74c3c','#f39c12'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=380, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2 ──────────────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### 📅 Global Sales by Year")
    year_df = filtered.groupby('Publish_Year')['Global_Sales'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=year_df['Publish_Year'], y=year_df['Global_Sales'],
                             fill='tozeroy', line=dict(color='#9b59b6', width=2.5),
                             fillcolor='rgba(155,89,182,0.15)', name='Global Sales'))
    fig.update_layout(height=320, xaxis_title='Year', yaxis_title='Sales (M)', margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown(f"#### 🏢 Top 10 Publishers — {sel_region}")
    pub_df = filtered.groupby('Publisher')[region_col].sum().nlargest(10).reset_index()
    pub_df.columns = ['Publisher','Sales']
    fig = px.bar(pub_df, x='Sales', y='Publisher', orientation='h',
                 color='Sales', color_continuous_scale='Purples',
                 text=pub_df['Sales'].apply(lambda x: f"{x:.1f}M"))
    fig.update_traces(textposition='outside')
    fig.update_layout(height=320, showlegend=False, coloraxis_showscale=False,
                      yaxis={'categoryorder':'total ascending'}, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3 ──────────────────────────────────────────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    st.markdown("#### 🏆 Top 10 Best-Selling Games")
    top_games = filtered.nlargest(10, 'Global_Sales')[['Game_Name','Global_Sales','Genre','Publisher','Publish_Year']]
    fig = px.bar(top_games, x='Global_Sales', y='Game_Name', orientation='h',
                 color='Genre', text=top_games['Global_Sales'].apply(lambda x: f"{x:.1f}M"),
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='outside')
    fig.update_layout(height=350, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.markdown("#### 🎯 Genre Performance by Region")
    genre_region = filtered.groupby('Genre')[['NA_Sales','EU_Sales','JP_Sales']].sum().reset_index().nlargest(8,'NA_Sales')
    fig = go.Figure()
    fig.add_trace(go.Bar(name='NA', x=genre_region['Genre'], y=genre_region['NA_Sales'], marker_color='#3498db'))
    fig.add_trace(go.Bar(name='EU', x=genre_region['Genre'], y=genre_region['EU_Sales'], marker_color='#2ecc71'))
    fig.add_trace(go.Bar(name='JP', x=genre_region['Genre'], y=genre_region['JP_Sales'], marker_color='#e74c3c'))
    fig.update_layout(barmode='group', height=350, margin=dict(l=0,r=0,t=10,b=0), xaxis_tickangle=30)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📋 View Raw Data"):
    show_cols = ['Game_Name','Genre','Publisher','Publish_Year','Global_Sales','NA_Sales','EU_Sales','JP_Sales','Other_Sales']
    st.dataframe(filtered[show_cols].sort_values('Global_Sales', ascending=False).head(500), use_container_width=True)

st.caption("🎓 Built by Sneha Shree M U | Data Analyst & Data Scientist | Bangalore")
