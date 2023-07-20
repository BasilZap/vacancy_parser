CREATE TABLE vacancy
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar,
	company_id int REFERENCES company(company_id) NOT NULL,
	salary_min	real,
	salary_max real,
	vacancy_link varchar,
	description text
);

CREATE TABLE company
(
	company_id int PRIMARY KEY,
	company_name varchar,
	company_link varchar,
	company_adress varchar,
	telephone varchar(20)
);