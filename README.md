Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализованы REST API по работе с меню ресторана, все CRUD операции. 

Запуск приложения

Для запуска приложения - "docker-compose -f docker-compose.yaml up -d" \
Тесты в Postman проходят, но в браузере нужно указывать порт 8000 а не 80 для доступа к документации /docs
Для остановки приложения - "docker-compose stop" \

Для запуска тестов - "docker-compose -f docker-compose-test.yaml up" \



ORM запрос реализован через @property

Был составлен sql запрос, который бы выдавал то что нужно, но его адаптация в orm запрос не увенчалась успехом. Поэтому выбрал был путь через @property. Вот сам запрос

    SELECT 
    m.*,
    (
        SELECT COUNT(*) 
        FROM submenus sm 
        WHERE sm.menu_id = m.id
    ) as submenus_count,
    (
        SELECT COUNT(*) 
        FROM dishes d 
        WHERE EXISTS (SELECT * FROM submenus sm WHERE sm.menu_id = m.id AND sm.id = d.submenu_id)
    ) as dishes_count
    FROM menus m;


Тесты на проверку кол-ва блюд и подменю в меню в файле test_dish_count.py в папке тест
