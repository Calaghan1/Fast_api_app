Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. 

Запуск приложения

Все команды выполняются из папки app

Шаг 1:  Поднимаем базу данных в докере командой     docker-compose up\
Шаг 2:  Активируем вирутальное окружение    source venv/bin/activate\
Шаг 3:  Устанавливаем зависимости                   pip3 install -r requirements.txt\
Шаг 4:  Запускаем сервер uvicorn командой           python3 -m uvicorn main:app --reload\
Шаг 5:  Запускаем тесты в postman\
