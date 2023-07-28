CREATE TABLE vacancy
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar,
	company_id int REFERENCES company(company_id) NOT NULL,
	salary_from	real,
	salary_to real,
	vacancy_url varchar,
	vacancy_description text
);

CREATE TABLE company
(
	company_id int PRIMARY KEY,
	company_name varchar,
	company_city varchar,
	company_site_url varchar,
	company_hh_url varchar,
	company_description text
);