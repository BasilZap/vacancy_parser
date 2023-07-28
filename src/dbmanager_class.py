import psycopg2
from src.headhunter_class import *

DB_CONNECTION = psycopg2.connect(host='localhost', database='headhunter', user='postgres', password='123456')
VACANCY_SQL_FILTER = "(%s, %s, %s, %s, %s, %s, %s)"
EMPLOYEE_SQL_FILTER = "(%s, %s, %s, %s, %s, %s)"


class DBManager:

    def __init__(self, connection):
        self.connection = connection

    def insert_data_into_db(self, data_filter: str, json_data: list, table_name: str):
        with self.connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                for custom_record in json_data:
                    cur.execute(f"INSERT INTO {table_name} VALUES {data_filter}", custom_record)
                conn.commit()  # Запись данных в таблицу customers
            cur.close()
#
    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass


""" Заполнение таблиц """
# employee_data = get_employee_items(get_employee_data(EMPLOYERS_DATA))
# vacancy_data = get_vacations_items(get_data_from_hh(EMPLOYERS_DATA))
# db_con = DBManager(DB_CONNECTION)
# db_con.insert_data_into_db(EMPLOYEE_SQL_FILTER, employee_data, 'company')
# db_con.insert_data_into_db(VACANCY_SQL_FILTER, vacancy_data, 'vacancy')
# DB_CONNECTION.close()
