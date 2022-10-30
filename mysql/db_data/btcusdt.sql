CREATE DATABASE IF NOT EXISTS btcusdt;
USE btcusdt;

CREATE TABLE IF NOT EXISTS datetime (
    time     DATETIME   NOT NULL  UNIQUE,
    PRIMARY KEY (time)
);

CREATE TABLE IF NOT EXISTS ohlcv (
    time  DATETIME   NOT NULL  UNIQUE   REFERENCES datetime(time),
    open     FLOAT      NOT NULL,
    high     FLOAT      NOT NULL,
    low      FLOAT      NOT NULL,
    close    FLOAT      NOT NULL,
    volume   FLOAT      NOT NULL,
    PRIMARY KEY (time)
);

CREATE TABLE IF NOT EXISTS orderbook_buy (
    time     DATETIME   NOT NULL  UNIQUE   REFERENCES datetime(time),
    price    FLOAT      NOT NULL,
    size     FLOAT      NOT NULL,
    PRIMARY KEY (time)
);

CREATE TABLE IF NOT EXISTS orderbook_sell (
    time     DATETIME   NOT NULL  UNIQUE   REFERENCES datetime(time),
    price    FLOAT      NOT NULL,
    size     FLOAT      NOT NULL,
    PRIMARY KEY (time)
);
