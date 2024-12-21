{{ config(
    materialized='view' 
) }}

SELECT
    ticker,
    CAST(strftime('%w', date_time) AS INT) AS date,
    date_time,
    close_price,
    volume
FROM
    {{ ref('stock_data_transformed') }}  -- Replace with your base model name
WHERE
    CAST(strftime('%w', date_time) AS INT) NOT IN (0, 6)  -- Exclude weekends (Sunday=0, Saturday=6)
