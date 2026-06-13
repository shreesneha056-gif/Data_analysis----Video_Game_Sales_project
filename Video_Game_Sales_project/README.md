# 🎮 Global Video Game Sales & Publisher Performance Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Database-MS%20SQL%20Server-blue?style=for-the-badge&logo=microsoft-sql-server" alt="SQL Server">
  <img src="https://img.shields.io/badge/Visualization-Power%20BI-yellow?style=for-the-badge&logo=power-bi" alt="Power BI">
  <img src="https://img.shields.io/badge/Language-T--SQL-red?style=for-the-badge" alt="TSQL">
</p>



## 📝 Description
This repository contains an end-to-end data analysis project that maps global video game historical transaction distributions from 1980 across regional footprints. Utilizing **T-SQL (MS SQL Server)** for multi-table relational inner joins, window functions (`LAG`), and database views, alongside an interactive **Power BI** report, this project tracks performance drivers by publishers, genres, platforms, and release dates.

---

## 🎯 Regional Distribution Footprint (KPIs)

| Market Region | Revenue Contribution | Core Strategic Percentage |
| :--- | :--- | :--- |
| 🇺🇸 **North America (NA Sales)** | **Top Leading Region** | **55.08%** of Global Revenue |
| 🇪🇺 **Europe (EU Sales)** | Second Tier Volume | **32.88%** of Global Revenue |
| 🇯🇵 **Japan (JP Sales)** | Concentrated Market Segment | **10.11%** of Global Revenue |
| 🌐 **Other Regions** | Rest of World Footprint | **1.94%** of Global Revenue |

---

## 🔍 Core Insights Discovered

* **🏆 Top All-Time Titles:** Historical data profiles prove major legacy titles like **Wii Sports**, **Super Mario Bros.**, and **Mario Kart Wii** represent massive individual distribution anomalies, driving dense peaks in cumulative volume.
* **📅 Temporal Performance Trends:** Cross-sectional aggregation by calendar periods shows distinct distribution variances when evaluating global sales metrics against previous year regional run rates.
* **🏬 Publisher Market Power:** High-volume legacy publishers maintain structural advantages, pulling in consistent multi-regional baseline revenues over dynamic lifecycle waves.

---

## 🛠️ Tech Stack & Tools Used
* **Database Engine:** Microsoft SQL Server (T-SQL)
* **BI & Data Visualization:** Power BI Desktop
* **Development Environment:** VS Code / Git Bash
* **Documentation Language:** Markdown

---

## 🗂️ Project Repository Structure
```text
├── Data/
│   ├── video_game_sales.csv       # Relational transaction sales ledger
│   ├── video_game_publishers.csv  # Publisher entity mapping table
│   ├── video_game_platforms.csv   # Hardware system platform metadata
│   └── video_game_genres.csv      # Classification genre metadata
├── SQL_Scripts/
│   └── Video_Games_Sales_project_SQL.sql # Analytical relational view definitions
├── Dashboard/
│   ├── Video_Game_Sales_image.pdf # Print layout export of the visualization
│   └── Video_Game_Sales_pdf.jpg   # High-resolution dashboard screen capture
└── README.md                      # Main project presentation documentation