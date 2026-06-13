Create database ecommerce_project;

Select * from ecommerce_sales;

Alter Table ecommerce_sales
Drop column column11,column12,column13,column14;

Select * from ecommerce_sales;

Select Sum(sales) as total_sales, Sum(Profit) as Total_profit,
round(sum(profit)/sum(sales),4) as profit_margin
from ecommerce_sales;


Create or alter view sales_by_region as
Select top 100  region, Sum(sales) as total_sales_of_product
from ecommerce_sales 
group by region
order by total_sales_of_product desc;

select * from sales_by_region

create or alter view sales_by_category as 
Select Top 100 category, Sum(sales) as total_sales_of_product
from ecommerce_sales 
group by category
order by total_sales_of_product desc;

Select * from sales_by_category

create or alter view monthly_trend as
Select top 100 [month], Sum(sales) as total_sales_of_product
from ecommerce_sales 
group by [month]
order by total_sales_of_product desc;

select * from monthly_trend

create or alter view top_products as
Select top 100 product_name , Sum(sales) as total_sales_of_product
from ecommerce_sales 
group by product_name
order by total_sales_of_product desc;

select * from top_products

create or alter view top_5_products as
Select top 5 product_name , Sum(sales) as total_sales_of_product
from ecommerce_sales 
group by product_name
order by total_sales_of_product desc;

select * from top_5_products