---

# Универсальный HTTP/HTTPS Прокси

## Описание

Проект представляет собой универсальный прокси-сервер, который принимает HTTP и HTTPS запросы на заданный порт и перенаправляет их на целевой сервер. Прокси логирует каждый приходящий запрос и имеет возможность автоматического обновления SSL-сертификатов через Let's Encrypt.

## Особенности

- Поддержка HTTP и HTTPS.
- Перенаправление всех видов HTTP методов, заголовков и тела запроса.
- Логирование входящих запросов.
- Автоматическое обновление SSL-сертификатов с помощью Let's Encrypt.
- Вынесение конфигурационных параметров в переменные окружения.
- Автономная работа без использования Nginx или Apache.
- Работа как системный сервис с автоматическим перезапуском при сбоях.
- Мультиплатформенность: реализации на Go, Python, Swoole (PHP), C#, и C++.

## Как использовать

1. Заполняем `config.ini` актуальными данными.
2. Кладем Python-скрипт и service-файлы в соответствующие папки.
3. Запускаем `setup.sh` с правами root.

Вот и всё, твой прокси должен запуститься и работать как надо.

---

### Сервисные файлы

Для Ubuntu создаем `proxy.service`:

Для Alpine создаем файл `proxy` в `/etc/init.d/`:

---

```shell
pip3 install Flask requests
```