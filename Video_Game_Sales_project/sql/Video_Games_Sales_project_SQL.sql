create database VideoGame_project


CREATE or ALTER VIEW total_of_all_sales AS
SELECT TOP 10000 P.publisher_name,ROUND(SUM(S.na_sales + S.eu_sales + S.jp_sales + S.other_sales),3)AS total_sales
FROM video_game_sales AS S
INNER JOIN video_game_publishers AS P
ON S.publisher_id = P.publisher_id
GROUP BY P.publisher_name
ORDER BY total_sales DESC;

SELECT * FROM total_of_all_sales



CREATE or ALTER VIEW top_1_publisher_name_by_game_name AS
SELECT TOP 1 P.publisher_name,COUNT(S.game_name) AS number_of_best_selling_games
FROM video_game_sales AS S
INNER JOIN video_game_publishers AS P
ON S.publisher_id = P.publisher_id
WHERE (S.na_sales + S.eu_sales + S.jp_sales + S.other_sales) > 10
GROUP BY P.publisher_name
ORDER BY number_of_best_selling_games DESC;

SELECT * FROM top_1_publisher_name_by_game_name



CREATE or ALTER VIEW publisher_total_sales_by_percentage AS
SELECT TOP 10000 P.publisher_name,ROUND(SUM(S.na_sales + S.eu_sales + S.jp_sales + S.other_sales),3) AS publisher_total_sales,
 ROUND(  ( ROUND(SUM(S.na_sales + S.eu_sales + S.jp_sales + S.other_sales),3) * 100.0 /
          (SELECT ROUND(SUM(na_sales + eu_sales + jp_sales + other_sales),3) FROM video_game_sales)
    ),3) AS percentage_contribution
FROM video_game_sales AS S
INNER JOIN video_game_publishers AS P
ON S.publisher_id = P.publisher_id
GROUP BY P.publisher_name
ORDER BY percentage_contribution DESC;

SELECT * FROM publisher_total_sales_by_percentage



CREATE or ALTER VIEW top_1_average_sales_per_games AS
SELECT TOP 1 P.publisher_name,ROUND(AVG(S.na_sales + S.eu_sales + S.jp_sales + S.other_sales),3) AS average_sales_per_game
FROM video_game_sales AS S
INNER JOIN video_game_publishers AS P
ON S.publisher_id = P.publisher_id
GROUP BY P.publisher_name
ORDER BY average_sales_per_game DESC;

SELECT * FROM top_1_average_sales_per_games



CREATE or ALTER VIEW top_1_month_growth_percentage AS
WITH Publishersales AS (
    SELECT TOP 100000
        publisher_ID,
        YEAR(publish_year) AS Year,
        MONTH(publish_year) AS Month,
        SUM(NA_Sales + EU_Sales + JP_Sales + Other_Sales) AS Total_Sales
    FROM video_game_sales
    GROUP BY Publisher_ID, YEAR(Publish_Year), MONTH(Publish_Year)
),
TopPublisher AS (
    SELECT TOP 1 Publisher_ID
    FROM video_game_publishers
    GROUP BY Publisher_ID 
),
TopPublisherSales AS (
    SELECT TOP 1000000
        ps.Publisher_ID,
        ps.Year,
        ps.Month,
        ps.Total_Sales,
        LAG(ps.Total_Sales) OVER (PARTITION BY ps.Publisher_id ORDER BY ps.Year, ps.Month) AS Prev_Month_Sales
    FROM PublisherSales ps
    WHERE ps.Publisher_ID = (SELECT Publisher_ID FROM TopPublisher)
)
SELECT TOP 100000
    Publisher_ID,
    Year,
    Month,
    Total_Sales,
    Prev_Month_Sales,
    CASE 
        WHEN Prev_Month_Sales = 0 OR Prev_Month_Sales IS NULL THEN NULL
        ELSE ((Total_Sales - Prev_Month_Sales) / Prev_Month_Sales) * 100
    END AS MoM_Growth_Percentage
FROM TopPublisherSales
ORDER BY Year, Month;

SELECT * FROM top_1_month_growth_percentage
