# foodgram
![Foodgram workflow](https://github.com/yanasedowa/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

### Описание

Проект **Foodgram** — онлайн-сервис «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Основной функционал:

> -   Регистрация на сайте или просмотр рецептов без регистрации

Для авторизованных пользователей доступно:

> -   Подписка (отписка) на автора
> -   Добавление (удаление) рецептов в Избранное
> -   Добавление (удаление) рецепта в Список покупок
> -   Скачивание файла (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из Списка покупок
> -   Создание (публикация, изменение, удаление) своего рецепта
> -   Изменение пароля

### http://62.84.120.127/

login: sedow
password: 541007fap

### Как запустить проект:

На macOS или Linux запустите программу Терминал. 
Если у вас Windows — запускайте [Git Bash](https://gitforwindows.org/)

Клонировать репозиторий и перейти в него в командной строке:


```

git@github.com:yanasedowa/foodgram-project-react.git

```
  

```

cd foodgram-project-react/infra

```

В файле `nginx.conf`:

```

`server_name`: публичный IP сервера

```

Скопировать файлы 'docker-compose.yaml' и 'nginx.conf' из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx.conf соответственно:

В локальном репозитории:

```

scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf

```


Заполнить данные в `Settings - Secrets - Actions secrets`:

```

DOCKER_USERNAME: логин в DockerHub
DOCKER_PASSWORD: пароль пользователя в DockerHub
HOST: публичный ip-адрес сервера
USER: логин на сервере
SSH_KEY: приватный ssh-ключ (cat ~/.ssh/id_rsa)
PASSPHRASE: eсли при создании ssh-ключа вы использовали фразу-пароль
DB_ENGINE: django.db.backends.postgresql
DB_HOST: db
DB_PORT: 5432
TELEGRAM_TO: id своего телеграм-аккаунта
TELEGRAM_TOKEN: токен бота
DB_NAME: postgres
POSTGRES_USER: postgres 
POSTGRES_PASSWORD: postgres
SECRET_KEY: key

```

Войти на свой удаленный сервер в облаке.

Остановить службу nginx:

```

sudo systemctl stop nginx

```

Установить docker и docker-compose:

```

sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

```

После деплоя будут созданы и запущены в фоновом режиме контейнеры (db, backend, frontend, nginx).

Приложение становится доступным по адресу http://localhost.

Заполнить базу тестовыми данными:

```

docker-compose exec web python manage.py uploadcsv

```


### Примеры запросов:

Получить список рецептов

Права доступа: Страница доступна всем пользователям

**GET**
http://localhost/api/recipes/

*Ответ*
**200**
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

Создать рецепт.

Права доступа: Доступно только авторизованному пользователю

**POST**
http://localhost/api/recipes/

*Передаваемые данные*

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

*Ответ*
**201**
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

*Ответ*
**400**
```
{
  "field_name": [
    "Обязательное поле."
  ]
}
```
Удалить рецепт.

Права доступа: Доступно только автору данного рецепта

**DELETE**
http://localhost/api/recipes/{id}/

Обновить рецепт

Права доступа: Доступно только автору данного рецепта

**PATCH**
http://localhost/api/recipes/{id}/

*Передаваемые данные*

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

*Ответ*
**200**
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

### Технологии

-   [Python](https://www.python.org/)
-   [Django](https://www.djangoproject.com/)
-   [Django REST framework](https://www.django-rest-framework.org/)
-   [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
-   [PostgreSQL](https://postgrespro.ru/docs/postgresql/12/)
-   [Gunicorn](https://gunicorn.org/)
-   [nginx](https://www.nginx.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [GitHub Actions](https://github.com/features/actions)


### Автор
Седова Яна, 33 когорта 
