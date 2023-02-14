# Django + Stripe API Payment Backend

Приложение, моделирующее процесс оплаты отдельных товаров, а также товаров, 
сгруппированных в заказы, про помощи фреймворка Django и библиотеки платежных функций 
Stripe (https://stripe.com/docs).


### Функционал
Реализованы Django-модели Item (отдельный товар), Order (заказ), Discount (скидка), Tax (налог). 
Присутствуют возможности выбора валюты заказа и товара, назначения заказу налога или скидки.
В модели товара также реализован метод, приводящий цену в формат, 
удобный для отображения, в модели заказа - методы расчета стоимости группы товаров 
и общей стоимости заказа. 

В приложении реализованы следующие эндпойнты:
1. ```GET /buy/{id}``` - возвращает Stripe Session Id для оплаты выбранного Item;
2. ```GET /item/{id}``` - возвращает простую HTML-страницу с информацией о выбранном Item и кнопкой Buy. 
При нажатии на Buy происходит запрос на ```/buy/{id}```, получение session_id и далее перенаправление 
на форму оплаты Stripe;
3. ```GET /buy/order/{id}``` - возвращает Stripe Session Id для оплаты выбранного Order;
4. ```GET /order/{id}``` - возвращает простую HTML-страницу с информацией о выбранном Order,
в т.ч. информацию о входящих в заказ товарах, их количестве и стоимости, а также общей 
стоимости заказа, и кнопкой Buy. 
При нажатии на Buy происходит запрос на ```/buy/order/{id}```, получение session_id и далее перенаправление 
на форму оплаты Stripe;
5. ```GET /success``` - выводит сообщение об успешном платеже. Запрос перенаправляется на эту страницу 
в случае успешного платежа;
6. ```GET /cancelled``` - выводит сообщение о прерванном платеже. Запрос перенаправляется 
на эту страницу в случае, если платеж был прерван;
7. ```GET /admin``` - панель администратора Django. Доступны для редактирования и создания 
новых записей модели Item, Order, Discount, Tax. 
8. ```GET /config``` - служебный эндпойнт, возвращающий публичный ключ Stripe.

### Запуск проекта
1. Копируем репозиторий и переходим в директорию проекта
```sh 
git clone git@github.com:artemyev1003/payments_backend.git
cd payments_backend
``` 
2. Собираем и запускаем проект:
```sh
docker-compose up --build
```
Формируются 2 контейнера - с Django-приложением и с БД PostreSQL. 
Для удобства тестирования приложения при первом запуске контейнера создается суперпользователь
(логин для входа по умолчанию - admin, пароль - admin),
а также выполняются миграции, в т.ч. миграция, записывающая в БД тестовые данные - 
два Item (id == 1 и id == 2) и два Order (id == 1 и id == 2).



