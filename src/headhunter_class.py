import requests
import json
import time

EMPLOYERS_DATA = {1740: "Яндекс", 1111058: "Rockit", 9187006: "Answeroom", 250: "Comtec Inc", 67611: "Тензор",
                  3177: "ПервыйБит", 1455: "HeadHunter", 906557: "СберТех", 41862: "Контур", 733: "Artezio"}


def get_data_from_hh(employers_dict: dict) -> list:
    """
    Функция получения данных по вакансиям от HH API
    Считывает максимально возможное количество вакансий
    по указанным работодателям и возвращает json raw список
    :param employers_dict: словарь с id и названиями работодателей
    :return: список raw json со всеми данными по вакансиям
    """
    json_data_list = []
    for employee in employers_dict:
        print(f'Считываются вакансии организации {employers_dict[employee]}')
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

    return json_data_list


def get_vacations_items(json_data_list: list) -> list:
    """
    Функция для обработки вакансий.
    Выбирает конкретные поля и объединяет в список кортежей.
    В случае отсутствия данных - формирует их.
    :param json_data_list: Список raw json со всеми данными по вакансиям
    :return: список кортежей с выбранными данными по вакансиям
    """
    vacation_item_list = []
    for items in json_data_list:
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


def get_employee_data(employers_dict: dict) -> list:
    """
    Функция получения данных по работодателям от HH API
    Считывает данные по указанным работодателям и возвращает json raw список
    :param employers_dict: словарь с id и названиями работодателей
    :return: список raw json со всеми данными по работодателям
    """
    json_data_list = []
    for employee_id in employers_dict.keys():
        print(f'Получение данных о работодателе {employers_dict[employee_id]}')
        recs = requests.get('https://api.hh.ru/employers/' + str(employee_id))
        json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
        json_data_list.append(json_record)

    return json_data_list


def get_employee_items(employers_list: list) -> list:
    """
    Функция для обработки данных работодателей.
    Выбирает конкретные поля и объединяет в список кортежей.
    В случае отсутствия данных - формирует их.
    :param employers_list: Список raw json со всеми данными по работодателям
    :return: список кортежей с выбранными данными работодателей
    """
    employee_item_list = []
    for items in employers_list:
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


# api_data = get_data_from_hh({41862: "Контур"})
# print(len(api_data))
# api_recs = get_vacations_items(api_data)
# print(api_recs)
# print(len(api_recs))
# emp = get_employee_data(EMPLOYERS_DATA)
# print(get_employee_items(emp))

"""employee_item_list.append({
             'id': items['id'],
             'name': items['name'],
             'city': items['area']['name'],
             'site_url': items['site_url'],
             'hh_url': items['alternate_url']
             })
        if items['industries'] != []:
            for recs in items['industries']:
                industries_record += '. ' + recs['name']
            employee_item_list[-1]['industries'] = industries_record
        else:
            employee_item_list[-1]['industries'] = 'Не указано.'"""