FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=root
ENV TZ: "Asia/Tokyo"

COPY ./mysql/config/my.cnf /etc/mysql/my.cnf
RUN chmod 644 /etc/mysql/my.cnf

COPY ./mysql/db_data/btcusdt.sql /docker-entrypoint-initdb.d/btcusdt.sql
