-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)
select c.company_name, concat(e.first_name, ' ', e.last_name)
from customers as c
join orders as o using(customer_id)
join employees as e using(employee_id)
join shippers as s ON o.ship_via = s.shipper_id
where c.city = 'London' and e.city = 'London' and s.company_name = 'United Package';

-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.
select p.product_name, p.units_in_stock, s.contact_name, s.phone from products as p
join categories as c using(category_id)
join suppliers as s using(supplier_id)
where p.discontinued=0 and p.units_in_stock<25 and (c.category_name='Dairy Products' or c.category_name='Condiments')
order by units_in_stock;

-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа
select company_name from customers as c
where c.customer_id not in (select customer_id from orders)

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
select product_name from products
where product_id in (select distinct product_id from order_details
where quantity=10)