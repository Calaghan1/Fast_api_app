Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализованы REST API по работе с меню ресторана, все CRUD операции. 

Запуск приложения

Для запуска приложения - docker-compose -f docker-compose.yaml up -d  или make start
Для запуска остановки приложения - docker-compose stop  или make stop

Для запуска тестов - docker-compose -f docker-compose-test.yaml up или make test