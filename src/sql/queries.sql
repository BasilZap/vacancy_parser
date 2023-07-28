SELECT COUNT(*) FROM vacancy
INNER JOIN company USING(company_id)

SELECT DISTINCT company_name, COUNT(*) FROM company
INNER JOIN vacancy ON vacancy.company_id=company.company_id
GROUP BY company_name

SELECT company_name, vacancy_name, salary_from, salary_to, vacancy_url FROM company
INNER JOIN vacancy ON vacancy.company_id=company.company_id

SELECT vacancy_name, AVG(salary_to + salary_from) AS salary FROM vacancy
GROUP BY vacancy_name
ORDER BY salary

--?

SELECT * FROM vacancy
WHERE vacancy_name LIKE '%Python%' OR vacancy_name LIKE '%python%'