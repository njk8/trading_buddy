-- models/stock_data_transformed.sql

with stock_data_source as (
    select
        ticker,
        date_time,
        close_price,
        volume
    from stock_data
)

select
    ticker,
    date_time,
    close_price,
    volume
from stock_data_source 
where date_time >= date('now', '-7 days')  -- Example: last 7 days
