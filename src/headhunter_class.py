import requests
import json
import time

EMPLOYERS_DATA = {1740: "Яндекс", 1111058: "Rockit", 9187006: "Answeroom", 250: "Comtec Inc", 67611: "Тензор",
                  3177: "ПервыйБит", 1455: "HeadHunter", 906557: "СберТех", 41862: "Контур", 733: "Artezio"}


class HeadHunterApi:

    def __init__(self, employee_dict: dict):
        self.employee_dict = employee_dict
        self.employee_json_data = []
        self.vacancy_json_data = []

    def get_data_from_hh(self):
        """
        Функция получения данных по вакансиям от HH API
        Считывает максимально возможное количество вакансий
        по указанным работодателям и возвращает json raw список.
        :return: Список raw json со всеми данными по вакансиям
        """
        json_data_list = []
        for employee in self.employee_dict:
            print(f'Считываются вакансии организации {self.employee_dict[employee]}')
            for pages in range(0, 20):  # Читаем в цикле все страницы данных по вакансиям
                params = {
                    'host': 'hh.ru',
                    'employer_id': employee,
                    'locale': 'RU',
                    'area': 113,
                    'page': pages,
                    'per_page': 100
                }
                recs = requests.get("https://api.hh.ru/vacancies", params)
                json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
                json_data_list.extend(json_record['items'])  # Добавляем данные каждой страницы в общий список
                if (json_record['pages'] - pages) <= 1:  # Если страниц меньше 20, дочитываем последнюю и прерываем цикл
                    break
                print(f'Загрузка страницы - {pages}')
                time.sleep(0.20)  # Задержка на запрос, чтобы не загружать сервер HH

        self.vacancy_json_data = json_data_list

    def get_vacations_items(self) -> list:
        """
        Функция для обработки вакансий.
        Выбирает конкретные поля и объединяет в список кортежей.
        В случае отсутствия данных - формирует их.
        :return: Список кортежей с выбранными данными по вакансиям
        """
        vacation_item_list = []
        for items in self.vacancy_json_data:
            vacancy_data_1 = (items['id'], items['name'], items['employer']['id'])

            if items['salary'] is not None:
                if items['salary']['from'] is not None:
                    salary_from = items['salary']['from']
                else:
                    salary_from = None
                if items['salary']['to'] is not None:
                    salary_to = items['salary']['to']
                else:
                    salary_to = None
            else:
                salary_from = None
                salary_to = None

            vacancy_data_2 = (salary_from, salary_to, items['alternate_url'], items['snippet']['requirement'])
            vacancy_data = vacancy_data_1 + vacancy_data_2
            vacation_item_list.append(vacancy_data)
        return vacation_item_list

    def get_employee_data(self):
        """
        Функция получения данных по работодателям от HH API
        Считывает данные по указанным работодателям и возвращает json raw список.
        :return: Список raw json со всеми данными по работодателям
        """
        json_data_list = []
        for employee_id in self.employee_dict.keys():
            print(f'Получение данных о работодателе {self.employee_dict[employee_id]}')
            recs = requests.get('https://api.hh.ru/employers/' + str(employee_id))
            json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
            json_data_list.append(json_record)

        self.employee_json_data = json_data_list

    def get_employee_items(self) -> list:
        """
        Функция для обработки данных работодателей.
        Выбирает конкретные поля и объединяет в список кортежей.
        В случае отсутствия данных - формирует их.
        :return: Список кортежей с выбранными данными работодателей
        """
        employee_item_list = []
        for items in self.employee_json_data:
            industries_record = ''
            employee_tuple_1 = (items['id'], items['name'], items['area']['name'],
                                items['site_url'])

            if items['industries'] != []:
                for recs in items['industries']:
                    industries_record += recs['name'] + '. '
                industries = industries_record
            else:
                industries = 'Не указано.'
            employee_tuple_2 = (items['alternate_url'], industries)
            employee_item_list.append(employee_tuple_1 + employee_tuple_2)
        return employee_item_list


# hh = HeadHunterApi({41862: "Контур"})
# api_data = hh.get_data_from_hh()
# print(len(api_data))
# api_recs = hh.get_vacations_items()
# print(api_recs)
# print(len(api_recs))
# hh.get_employee_data()
# print(hh.get_employee_items())
