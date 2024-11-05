# Назначение приложения

Приложение разрабатывается для управления личными данными пользователя на его 
аккаунте сайта hh.ru через взаимодействие с API hh.ru. Данный инструмент 
поможет упростить процесс поиска вакансий, управлением личными данными и получением 
важных уведомлений.

### Основные операции
* Управление личными данными: обновление, изменение и удаление личных данных пользователя.
* Управление резюме: добавление, изменение, удаление и публикация резюме. Включает в себя 
также клонирование и проверку возможности создания нового резюме.
* Управление поисковыми фильтрами: настройка и применение фильтров для поиска вакансий, что позволит пользователям 
быстро находить подходящие рабочие места.
* Уведомления: получение уведомлений о появлении подходящих вакансий через Telegram и электронную 
почту, обеспечивая оперативную информацию о новых возможностях.
* Статистика и аналитика: составление статистики и аналитики по рынку труда, позволит пользователям
лучше понимать текущие тенденции и сделать более осознанные решения о своей карьере.

### Цель
Главная цель приложения — предоставить пользователям удобный и эффективный способ управления их 
личными данными и поиска вакансий. Приложение поможет сделать процесс построения карьерного пути 
более осознанным и информированным. Благодаря оперативным уведомлениям о новых вакансиях и важных 
событиях, пользователи будут в курсе актуальных возможностей. Кроме того, приложение даст возможность
анализировать рынок труда, что поможет пользователям лучше понимать свои финансовые перспективы и 
принимать обоснованные решения. Также это будет полезно и для работодателей.



## Документация

* hhru API.  Подробная документация доступна по адресу:  https://api.hh.ru/openapi/redoc#section/Obshaya-informaciya
* hhru API на GitHub: дополнительная информация и библиотеки доступны на https://github.com/hhru/api

# Структура Проекта

## Общая Информация
Проект строится на микросервисной архитектуре, что позволяет разделить сложное приложение на 
несколько автономных и управляемых компонентов. Это повышает гибкость разработки, 
масштабируемость и отказоустойчивость системы.

## Директории и Компоненты

### 1. Бэкэнд.
Директория backend/ содержит все бэкенд компоненты проекта.
Микросервисы

    authentication/
        Микросервис для регистрации пользователей.
        Технологии: Python Django
        База данных: PostgreSQL № 1
        Описание: Обеспечивает процесс регистрации пользователей, хранит и управляет учетными записями.
    authorization/
        Микросервис для авторизации пользователей.
        Технологии: Python Flask
        База данных: PostgreSQL № 1
        Описание: Обеспечивает процесс авторизации пользователей, управляет доступом и правами.
    data_collection/
        Микросервис для взаимодействия с API hh.ru (сбор и отправка данных).
        Технологии: Python Flask
        База данных: MongoDB №2
        Описание: Собирает и отправляет данные через API hh.ru, обрабатывает и хранит полученные данные.
    data_processing/
        Микросервис для обработки данных.
        Технологии: Java Spring Boot
        База данных: MongoDB №2
        Описание: Обрабатывает собранные данные, выполняет необходимые вычисления и преобразования.
    notification/
        Микросервис для отправки уведомлений через Telegram API.
        Технологии: Python Flask
        База данных: PostgreSQL № 3
        Описание: Отправляет уведомления пользователям через Telegram, хранит историю уведомлений.
    payment_service/
        Микросервис для осуществления платежей.
        Технологии: Java Spring Boot
        База данных: PostgreSQL № 4
        Описание: Обеспечивает процесс финансовых транзакций, хранит и управляет финансовыми данными.

### 2. Фронтенд
Директория frontend/ содержит все фронтенд компоненты проекта.
Приложения

    react-app/
        Реакт-приложение для веб-интерфейса.
        Описание: Предоставляет пользовательский интерфейс для взаимодействия с бэкенд-сервисами.
    kotlin-mobile-app/
        Будущее мобильное приложение на Kotlin.
        Описание: Разрабатывается для предоставления мобильного доступа к функционалу приложения.

### 3. Оркестрация
Директория orchestration/ содержит конфигурации и DAGs для оркестрации задач.
Airflow

    airflow/
        Конфигурации и DAGs для Airflow.
        Описание: Управляет выполнением задач по сбору, обработке и отправке данных, а также другими периодическими задачами.

### 4. Докер-контейниризация
Директория docker/ содержит файлы Docker и docker-compose.
Docker Файлы

    Dockerfile для каждого микросервиса.
    docker-compose.yml для оркестрации контейнеров.

### 5. Вспомогательные Файлы

    .env
        Файл для переменных окружения.
        Описание: Хранит конфигурационные переменные для различных окружений.
    README.md
        Файл с документацией проекта.
        Описание: Содержит информацию о структуре проекта, технологиях, использованных в разработке, и инструкции по запуску.

## Базы Данных
### Первая База Данных (PostgreSQL) - Аутентификация, Авторизация

    Аутентификация и Авторизация
        PostgreSQL хорошо подходит для этих сервисов из-за его поддержки реляционных данных и механизмов аутентификации и авторизации.
        Используются роли, пользователи и группы для управления доступом, а также различные методы аутентификации.

### Вторая База Данных (MongoDB) - Сбор Данных, Подготовка Данных

    Сбор Данных
        MongoDB подходит для обработки больших объемов неструктурированных или полуструктурированных данных.
        Используется для хранения и обработки данных, собранных из различных источников.
    Подготовка Данных
        MongoDB также используется для подготовки данных, особенно если данные требуют гибкой схемы и высокой скорости обработки.

### Третья База Данных (PostgreSQL) - Уведомления

    Уведомления
        PostgreSQL используется для хранения истории уведомлений.
        Для самого процесса отправки уведомлений можно использовать очередь сообщений типа RabbitMQ или Apache Kafka.

### Четвертая База Данных (PostgreSQL) - Оплата

    Оплата
        PostgreSQL используется для финансовых транзакций из-за его поддержки ACID и транзакционных операций.
        Критически важно для финансовых данных, хотя функциональность может быть вынесена в отдельную базу данных.


# Файловая Структура

Файловая структура проекта на данный момент такая, в дальнейшем возможны изменения:

```markdown
<pre>
├── backend/
│   ├── authentication/
│   │   └── ...
│   ├── authorization/
│   │   └── ...
│   ├── data_collection/
│   │   └── ...
│   ├── data_processing/
│   │   └── ...
│   ├── notification/
│   │   └── ...
│   └── payment_service/
│       └── ...
├── frontend/
│   ├── react-app/
│   │   └── ...
│   └── kotlin-mobile-app/
│       └── ...
├── orchestration/
│   └── airflow/
│       └── ...
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env
└── README.md
</pre>

