
  
    
    
    create  table main."create_tables"
    as
        -- models/create_tables.sql

CREATE TABLE IF NOT EXISTS stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date_time DATETIME NOT NULL,
    open_price REAL NOT NULL,
    high_price REAL NOT NULL,
    low_price REAL NOT NULL,
    close_price REAL NOT NULL,
    volume INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trade_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    trade_type TEXT NOT NULL,  -- buy/sell
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    trade_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

  