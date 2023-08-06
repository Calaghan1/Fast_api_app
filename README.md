Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализованы REST API по работе с меню ресторана, все CRUD операции.

Запуск приложения

Для запуска приложения - "docker-compose -f docker-compose.yaml up -d" \
Тесты в Postman проходят, в браузере нужно указывать порт 8000 для доступа к документации /docs \
Для остановки приложения - "docker-compose stop" \

Для запуска тестов - "docker-compose -f docker-compose-test.yaml up" \
