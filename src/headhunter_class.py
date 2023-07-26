import requests
import json
import time

EMPLOYERS_DATA = {1740: "Яндекс", 1111058: "Rockit", 9187006: "Answeroom", 250: "Comtec Inc", 67611: "Тензор",
                  3177: "ПервыйБит", 1455: "HeadHunter", 906557: "СберТех", 41862: "Контур", 733: "Artezio"}


def get_data_from_hh(employers_dict: dict) -> list:
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

    vacation_item_list = []
    for items in json_data_list:
        vacancy_data = {"id": items['id'], "name": items['name'], "company_id": items['employer']['id']}

        if items['salary'] is not None:
            if items['salary']['from'] is not None:
                vacancy_data["salary_from"] = items['salary']['from']
            else:
                vacancy_data["salary_from"] = None
            if items['salary']['to'] is not None:
                vacancy_data["salary_to"] = items['salary']['to']
            else:
                vacancy_data["salary_to"] = None
        else:
            vacancy_data["salary_from"] = None
            vacancy_data["salary_to"] = None

        vacancy_data["url"] = items['alternate_url']
        vacancy_data["description"] = items['snippet']['requirement']
        vacancy_data["name"] = items['name']
        vacation_item_list.append(vacancy_data)
    return vacation_item_list


def get_employee_data(employers_dict: dict) -> list:

    json_data_list = []
    for employee_id in employers_dict.keys():
        print(f'Получение данных о работодателе {employers_dict[employee_id]}')
        recs = requests.get('https://api.hh.ru/employers/' + str(employee_id))
        json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
        json_data_list.append(json_record)

    return json_data_list


def get_employee_items(employers_list: list) -> list:

    employee_item_list = []
    for items in employers_list:
        industries_record = ''
        employee_item_list.append({
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
            employee_item_list[-1]['industries'] = 'Не указано.'

    return employee_item_list


# api_data = get_data_from_hh({9187006: "Answeroom"})
# print(len(api_data))
# api_recs = get_vacations_items(api_data)
# print(api_recs)
# print(len(api_recs))
# emp = get_employee_data(EMPLOYERS_DATA)
# print(get_employee_items(emp))
