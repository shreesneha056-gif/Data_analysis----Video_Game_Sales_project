# 🎮 Sports Global Sales Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

> Interactive Streamlit dashboard replicating a Power BI report — analyzing global video game sales (1980–2016) across regions, genres, publishers, and top-selling games.

---

## 🎯 Dashboard Overview

| KPI | Value |
|-----|-------|
| Total EU Sales % | 10.11% |
| Total NA Sales % | 55.08% |
| Total JP Sales % | 32.88% |
| Total Other Sales % | 1.94% |
| Total Global Sales | 8,916 |

## 📊 Charts (exact Power BI replica)

- **4 Donut KPI Cards** — EU Sales % (cyan) / NA Sales % (blue) / JP Sales % (purple) / Other Sales % (amber)
- **4 Top Game Buttons** — Wii Sports / Super Mario Bros / Mario Kart Wii / Wii Sports Resort
- **Decomposition Tree** — Total Global Sales by Day Name → Month → Year
- **Column Chart** — Sum of Total Sales by Game Name (top 10)

## 🔽 Filters
- Genre dropdown (Action / Sports / Racing / RPG etc.)
- Year range slider (1980–2016)
- Clear all slicers button

## 🛠️ Tech Stack
- **Dashboard:** Streamlit, Plotly
- **Data:** Python, Pandas, SQL (MS SQL Server — T-SQL joins, LAG window functions)
- **BI Tool:** Power BI (original design)
- **Deployment:** Streamlit Community Cloud

## 📂 Project Structure
```
video-game-sales-analysis/
├── app.py               # Streamlit dashboard app
├── vg_sales.csv         # Game sales dataset (16,594 records)
├── vg_genres.csv        # Genre lookup
├── vg_publishers.csv    # Publisher lookup
├── requirements.txt     # Dependencies
├── Video_Game_Sales_project/
│   ├── Data/            # Raw CSV data
│   ├── sql/             # SQL queries
│   └── DashBoard/       # Power BI screenshots
└── README.md
```

## 🚀 How to Run Locally
```bash
git clone https://github.com/shreesneha056-gif/video-game-sales-analysis.git
cd video-game-sales-analysis
pip install -r requirements.txt
streamlit run app.py
```

---
📫 [LinkedIn](https://www.linkedin.com/in/sneha-shree-mu/) | [Portfolio](https://shreesneha056-gif.github.io/portfolio_website/) | [GitHub](https://github.com/shreesneha056-gif)
