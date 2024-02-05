"""Скрипт для заполнения данными таблиц в БД Postgres."""
import pandas as pd
import psycopg2

employees = pd.read_csv('north_data/employees_data.csv').values.tolist()
customers = pd.read_csv('north_data/customers_data.csv').values.tolist()
orders = pd.read_csv('north_data/orders_data.csv').values.tolist()
conn = psycopg2.connect(host='localhost', database='north', user='postgres', password='1405')
try:
    with conn:
        with conn.cursor() as cur1:
            cur1.executemany('insert into employees values(%s, %s, %s, %s, %s, %s)', employees)
        with conn.cursor() as cur2:
            cur2.executemany('insert into customers values(%s, %s, %s)', customers)
        with conn.cursor() as cur3:
            cur3.executemany('insert into orders values(%s, %s, %s, %s, %s)', orders)
finally:
    conn.close()
