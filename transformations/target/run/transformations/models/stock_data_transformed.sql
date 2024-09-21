
    
    create view main."stock_data_transformed" as
    -- models/stock_data_transformed.sql

with stock_data as (
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
from stock_data
where date_time >= date('now', '-7 days')  -- Example: last 7 days;