-- Скрипт настройки базы данных для percival-cargo

-- 1. Создание пользователя (если не существует)
DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'allocation') THEN
      CREATE USER allocation WITH PASSWORD 'allocation123';
   END IF;
END
$$;

-- 2. Создание базы данных (если не существует)
SELECT 'CREATE DATABASE allocation_db OWNER allocation'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'allocation_db')\gexec

-- 3. Подключение к новой базе данных
\c allocation_db

-- 4. Настройка прав на схему public
ALTER SCHEMA public OWNER TO allocation;
GRANT ALL ON SCHEMA public TO allocation;
GRANT CREATE ON SCHEMA public TO allocation;
GRANT USAGE ON SCHEMA public TO allocation;

-- 5. Настройка прав по умолчанию
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO allocation;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO allocation;

-- 6. Создание таблиц (если нужно вручную)
-- Таблица batches
CREATE TABLE IF NOT EXISTS batches (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(255) NOT NULL,
    sku VARCHAR(255) NOT NULL,
    _purchased_quantity INTEGER NOT NULL,
    eta DATE
);

-- Таблица order_lines (если нужна)
CREATE TABLE IF NOT EXISTS order_lines (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(255),
    sku VARCHAR(255),
    qty INTEGER NOT NULL
);

-- Вывод информации
\dt