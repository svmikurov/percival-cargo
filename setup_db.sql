-- Скрипт ПЕРЕСОЗДАНИЯ базы данных для percival-cargo
-- ВНИМАНИЕ! Удаляет существующую базу данных!

-- 1. Завершить все соединения с базой allocation
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'allocation';

-- 2. Удалить базу данных
DROP DATABASE IF EXISTS allocation;

-- 3. Удалить пользователя
DROP USER IF EXISTS allocation;

-- 4. Создать пользователя
CREATE USER allocation WITH PASSWORD 'abc123';

-- 5. Создать базу данных
CREATE DATABASE allocation OWNER allocation;

-- 6. Подключиться к новой базе
\c allocation

-- 7. Настройка прав
ALTER SCHEMA public OWNER TO allocation;
GRANT ALL ON SCHEMA public TO allocation;
GRANT CREATE ON SCHEMA public TO allocation;
GRANT USAGE ON SCHEMA public TO allocation;

-- 8. Права по умолчанию
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO allocation;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO allocation;

-- 9. Создание таблиц
CREATE TABLE batches (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(255) NOT NULL,
    sku VARCHAR(255) NOT NULL,
    _purchased_quantity INTEGER NOT NULL,
    eta DATE
);

CREATE TABLE order_lines (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(255),
    sku VARCHAR(255),
    qty INTEGER NOT NULL
);

-- 10. Вывод информации
\dt