# Library API

Backend-сервис для управления библиотекой (Регистрация книг, читателей, выдача книг, администраторы).

## Словарь:
БЛ = Бизнес Логика
borrow = Это фиксированный выдача книг
Активный книга = это книга который взято и пока не вернули
Копия = Экземпляр

## Как запустить проект:

Клонирование от github
```bash
git clone https://github.com/barstars/library.git
cd library
```

Войти на виртуальный окружение:
```bash
python -m venv venv
venv\Scripts\activate    # Для Windows
source venv/bin/activate # Для Linux/Mac
```

Установка зависимости:
```bash
pip install -r requirements.txt
```
Затем нужно создать файл .env и написать туда:

DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database
ACCESS_TOKEN_EXPIRE_DAYS=30 # JWT Будет хранится 30 дней
SECRET_KEY=supersecret      # Ключ для JWT
HESHALGORITHM=HS256         # Алгоритм для JWT

Затем нужно выполнить миграций Alembic
```bash
alembic upgrade head
```

Затем нужно Регистрировать первый Администратор. Но с ним можно и потом добавить администратор
```bash
python create_admin.py #Нужно будет написать Имя, email, Пароль
```
Теперь можно запустить сервер
```bash
uvicorn app.main:app
```

## Работа с API:
Ответы:
Если данные правильные и ответ положительный то ответ будет в формате:
status_code=200
```json
{
	"success":true,
	"message":"'Успех' или другие сообщение"
}
```

А если не удалось то ответ будет в формате:
```json
{
	"success":false,
	"message":"'email уже существует' или другие сообщение"
}
```

### Администратор может:
Регистрация админа:
url: /admin/register
Метод: post
json:
```json
{
	"username":"admin",
	"email": "admin",
	"password": "admin"
}
``` 

Войти на админа:
url: /admin/login
Метод: post
json:
```json
{
	"email": "admin",
	"password": "admin"
}
``` 

Регистрация книги:
url: /book/register
Метод: post
json:
```json
{
	"name":"admin",
	"author": "admin",
	"year": "admin",   # Можно и не написать
	"isbn": "admin",   # Можно и не написать
	"copies": "admin"  # Можно и не написать по умолчанию 1 не меньше 0
}
``` 

Регистрация читателья:
url: /reader/register
Метод: post
json:
```json
{
	"username":"pipl",
	"email": "pipl",
	"password": "pipl"
}
``` 

Удалить книгу со всеми borrows:
url: /book/delete
Метод: delete
json:
```json
{
	"id":"isdcbnckwjenkljnll-sdv-f-wse-fw-sds", # Нужно jwt_id от книги. его можно взять от /book
}
``` 

Добавить экземпляр на книгу:
url: /book/register/add
Метод: put
json:
```json
{
	"id":"isdcbnckwjenkljnll-sdv-f-wse-fw-sds", # Нужно jwt_id от книги. его можно взять от /book
	"copies": 1   # Сколько экземпляров нужно добавить. Число может быть меньше 0, чтобы уменшить экземпляр
}
``` 


### Читатель может:
Войти на читателья:
url: /reader/login
Метод: post
json:
```json
{
	"email": "pipl",
	"password": "pipl"
}
``` 

Взять книгу:
url: /book/borrow
Метод: post
json:
```json
{
	"id":"isdcbnckwjenkljnll-sdv-f-wse-fw-sds" # Нужно jwt_id от книги. его можно взять от /book
}
``` 

Вернуть книгу:
url: /book/returnbook
Метод: post
json:
```json
{
	"id":"afegsrhdjfh,gmgnfbdvaserhjthmnge5htyfg" # Нужно jwt_borrow_id от borrow. его можно взять от /book/getborrows/active
}
``` 

Узнать все borrows:
url: /book/getborrows/all
Метод: get
json: Не нужно

Узнать все активных borrows. То есть книги который ещё не вернулся:
url: /book/getborrows/active
Метод: get
json: Не нужно


### Все может:
Узнать все книги:
url: /book
Метод: get
json: Не нужно


## Структура проекта:
library/
       /app/
           /api/
               /admin/  # Здесь все API который начинается с /admin и работа только с ним
                     /register.py # Регистрация
                     /login.py    # Логин
                     /router.py   # начало ветки /admin
               /book/   # Здесь все API который начинается с /book и работа только с ним
                    /register.py           # API /register Регистрация
                    /home.py               # API / Там есть /book который покажет всех книг
                    /borrow_book.py        # API /borrow Чтобы взять книгу
                    /delete.py             # API /delete Удаление книги
                    /get_reader_borrows.py # API /getborrows Покажет либо все /all либо ещё не возврщённых книг /active.
                    /return_book.py        # API /returnbook Возвращает книгу
                    /router.py             # начало ветки /book
               /reader/ # Здесь все API который начинается с /reader и работа только с ним
                      /register.py # Регистрация
                      /login.py    # Логин
                      /router.py   # начало ветки /reader
           /core/
                /config.py # Здесь все глобальные переменные от .env
           /db/
              /crud/
                   /admin.py       # DataBaseManager для админ
                   /book.py        # DataBaseManager для книг
                   /reader.py      # DataBaseManager для читателей
                   /borrow_book.py # DataBaseManager для borrow
              /base.py    # Класс Base
              /session.py # Оттуда нужно взять db переменную как сессию чтобы работать с БД
           /models/
                  /admin.py       # Все модели для админ
                  /book.py        # Все модели для книг
                  /reader.py      # Все модели для читателей
                  /borrow_book.py # Все модели для borrow
           /services/
                    /auth/
                         /admin_auth.py  # Логин и регистрация админа 
                         /book_auth.py   # Регистрация книги, добавляем экземпляр и удаление
                         /reader_auth.py # Логин и регистрация читателья
                    /verification.py     # Узнаем что данные есть в БД через jwt id и возвращаем либо False либо данные от id прямо от БД
                    /password_hashing.py # Хэширование и проверка паролья
                    /get_data.py         # Изменяет данные на нужный формат и есть функция где можно получить все книги (Нужно изменить структуру. А пока так сойдёт)
                    /generate_jwt.py     # Генерирует и читает JWT
                    /book_use.py         # Работает с book. То есть возвращает, создаёт новый borrow, узнаёт какие есть borrow конкретного читателья
           /utils/    # Не используется. Здесь работает отправка сообщений на email или на другие платформы
           /main.py   # Запуск проекта
       /test/
       /alembic
       /create_admin.py  # Здесь добавляется новый админ без запуска сервера
       /alembic.ini
       /.env             # Здесь зависимоть переменное как DATABASE_URL и так далее
       /requirements.txt # Зависимости python


## Принятый решение и обяснение:

### База данных решение и обеснение:

Админ
название таблицы: "admin"
столбцы:
	id: Тип=UUID, primary_key=True, умолчанию=uuid.uuid4
	username: тип=str
	email: тип=str, уникальный=True
	password_hash: тип=str
Обяснение:
password_hash: хэшировать и потом сохранить нужно а не сразу

Borrow для книги
название таблицы: "borrowed_books"
столбцы:
	id: Тип=UUID, primary_key=True, умолчанию=uuid.uuid4
    reader_id: Тип=UUID, связано_с = reader.id удаляются данные когда удаляют reader.id
    book_id: Тип=UUID, связано_с = book.id удаляются данные когда удаляют book.id
    borrow_date: Тип=datetime.datetime, умолчанию=datetime.datetime.utcnow
    return_date: Тип=datetime.datetime могут_быть_None=True
Обяснение:
borrow_date: Не нужно добавить данные когда создают. Данные сам создатся когда создаются данные
return_date: Заполнится когда книгу возвращает. До этого всегда None
Решение:
Здесь хронится borrow, то есть здесь хронится id читателья и книги, время когда читатель взял и вернул, И id сомой данных.

Читатель
название таблицы: "reader"
столбцы:
	id: Тип=UUID, primary_key=True, умолчанию=uuid.uuid4
	username: тип=str
	email: тип=str, уникальный=True
	password_hash: тип=str
Обяснение:
password_hash: хэшировать и потом сохранить нужно а не сразу

Книга
название таблицы: "book"
столбцы:
	id: Тип=UUID, primary_key=True, умолчанию=uuid.uuid4
	name: тип=str
    author: тип=str
    year: тип=int, могут_быть_None=True
    isbn: тип=int, уникальный=True, могут_быть_None=True
    copies: тип=int умолчанию=1
    description: тип=str, могут_быть_None=True

### Другие решение и обеснение:
Всех книг могут любой:
Всех книг могут любой потому что, если человек не знает что ему нужно или не знает что там есть то люди не будет регистрироватся. То есть это как триллер фильма.


## Как реализована БЛ:
Все БЛ находится в app/services/book_use.py Потому что все БЛ связано с использванием книги.
Все БЛ находится внутри классе NewBorrowedBook потому что имменно там создаются новый borrow.
Для того чтобы создать новый borrow вызовается функция new_borrow. Сперва мы узнаем сколько у пользвателя активных книг. Потом узнаём взял ли у этот читатель такую книгу, через reader_id и book_id. И ещё узнаём сколько копий доступно. Потом проверяем. Если хотябы один из них будет не соответствовать нашем требованиям то borrow не создатся, инача продалжается. Потом исполняются функция add_borrow. Там мы сперва пытаемся уменшить количества копий книг. Если удалось то просто добавляем новый borrow.

Когда читатель хочет вернуть книгу он отправит JWT который хронится id этого borrow. А сервер через этот id найдёт этот borrow, увеличовает на 1 копий книг и дописовает return_date время и оно перестанет быть None, то есть книга будет как возвращена.

## Как реализуется аутентификации:

### Предупреждение
Все регисраций, удаление и изменение копий книг могут только Админ
Все хэширование паролья присходит когда регистрируется. А потом просто проверяются без дехэшируя пароль.
Все генерация JWT использует один и тот же пароль, дней и алгоритм. Для этого нужно dict. Для того чтобы показать или изменить cookie id обйзательно применяются JWT. То есть для того чтобы показать какие все книги мы их id сделам jwt и покажем как id. Все id который отправляют на БД они все jwt.
Используется библиотеки для хэширование и генераций JWT:
python-jose[cryptography] -> для генераций и чтение JWT
passlib[bcrypt]           -> для хэширование пароля
bcrypt<4.1.0              -> откат версию чтобы passlib работал с паролями

### Админ:
/admin/register
Отправляются данные username, email, password. Мы сперва узнаём что отправитель запроса админ через Cookies в is_admin из app/services/verification.py. Потом пытаемся регистрировать. Если вышло ошибка то это значит что это из за email который уже существует. Иначе мы получим id. Но мы не отправим этот id мы просто возвращаем что зарегистрировано.

/admin/login
Отправляются данные email, password. Мы узнаём от БД что этои данные правилны или нет. Если правильно то просто изменим Cookies пользвателья на {"id":jwt}. И возвращаем что вошли.

### Читатель:
/reader/register
То же самое что админ но на другом БД

/reader/login
То же самое что админ но на другом БД

### Книга
/book/register
То же самое что админ но на другом БД и с другими данными(Нужные данные указано в "База данных решение и обеснение")

## Идея
Возможность оценить книгу.
Для реализаций нужно будет добавить несколько столбцов на БД. Для book столбец с средний оценкой и сколько человек оценил книгу. Он будет увеличоватся только тогда когда читатель возмёт эту книгу и оценит его, и тогда увеличется на 1 и изменится столбец с средний оценкой. А для borrowed_books нужно добавить оценку от читателья. И тогда пользватель могут потом изменить оценку или не оценить вообще.