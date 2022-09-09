# foodgram
![Django-app workflow](https://github.com/yanasedowa/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

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


### Как запустить проект:

На macOS или Linux запустите программу Терминал. 
Если у вас Windows — запускайте [Git Bash](https://gitforwindows.org/)

Клонировать репозиторий и перейти в него в командной строке:


```

git@github.com:yanasedowa/foodgram-project-react.git

```
  

```

cd yamdb_final/infra/nginx

```

В файле `default.conf`:

```

`server_name`: публичный IP сервера

```

Скопировать файлы 'docker-compose.yaml' и 'nginx/default.conf' из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно:

В домашней директории на сервере:

```
mkdir nginx

```

В локальном репозитории:

```

scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>:/home/<username>/nginx/default.conf

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

docker-compose exec web python manage.py loaddata fixtures.json

```

Документация к проекту:

http://127.0.0.1:8000/redoc

### Примеры запросов:

Получить список всех категорий

Права доступа: Доступно без токена

**GET**
/http://localhost/api/v1/categories/

*Ответ*
**200**
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

Создать категорию.

Права доступа: Администратор.

Поле slug каждой категории должно быть уникальным.

**POST**
http://localhost/api/v1/categories/

*Передаваемые данные*

```
{
  "name": "string",
  "slug": "string"
}
```

*Ответ*
**201**
```
{
  "name": "string",
  "slug": "string"
}
```

*Ответ*
**400**
```
{
  "field_name": [
    "string"
  ]
}
```
Удалить категорию.

Права доступа: Администратор.

**DELETE**
http://localhost/api/v1/categories/{slug}/

Обновить информацию о произведении

Права доступа: Администратор

**PATCH**
http://localhost/api/v1/titles/{titles_id}/

*Передаваемые данные*

```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

*Ответ*
**200**
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
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
