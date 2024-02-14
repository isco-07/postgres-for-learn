import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print("FOREIGN KEY успешно добавлены")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    try:
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {db_name}")
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
    return


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    try:
        with open(script_file, 'r', encoding='utf-8') as script:
            cur.execute(script.read())
    except FileNotFoundError as e:
        print(f"Error opening script file: {e}")
    except psycopg2.Error as e:
        print(f"Error executing SQL script: {e}")


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS suppliers 
            (
                supplier_id SERIAL PRIMARY KEY
            )
        """)
    except psycopg2.Error as e:
        print(f"Error creating suppliers table: {e}")


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            suppliers_data = json.load(file)
        return suppliers_data
    except FileNotFoundError as e:
        print(f"Error opening JSON file: {e}")
        return []


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    try:
        for i in suppliers[0].keys():
            cur.execute(f"alter table suppliers add column {i} varchar")
        for supplier in suppliers:
            columns_str = ', '.join(supplier.keys())
            values_str = ', '.join([f"%({column})s" for column in supplier.keys()])
            sql_statement = f"INSERT INTO suppliers ({columns_str}) VALUES ({values_str});"
            cur.execute(sql_statement, supplier)
    except psycopg2.Error as e:
        print(f"Error inserting data into suppliers table: {e}")


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    pass


if __name__ == '__main__':
    main()
