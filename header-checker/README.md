# Header checker

Скрипт на Python, который запрашивает один или несколько URL и проверяет,
отдаёт ли сервер основные заголовки безопасности: `X-Frame-Options`,
`X-Content-Type-Options`, `Content-Security-Policy` и `Referrer-Policy`.

## Запуск
```
uv run python src/header_checker/checker.py https://example.com https://example.org
```
Можно передать любое количество URL через пробел. Без аргументов скрипт
выводит подсказку по использованию и завершается с кодом 1.

Для проверки без выхода в интернет есть тестовый сервер на `127.0.0.1:8005`:
```
python tools/server.py
uv run python src/header_checker/checker.py http://127.0.0.1:8005/secure http://127.0.0.1:8005/weak
```
`/secure` отдаёт все четыре заголовка, `/weak` только `X-Content-Type-Options`,
остальные пути отвечают 404.

## Что это проверяет
| Заголовок | От чего защищает |
|---|---|
| X-Frame-Options | clickjacking: встраивание страницы в чужой iframe |
| X-Content-Type-Options | MIME sniffing: браузер не угадывает тип файла сам |
| Content-Security-Policy | XSS: ограничивает, откуда можно загружать скрипты и ресурсы |
| Referrer-Policy | утечка адреса страницы в заголовке Referer на другие сайты |

## Пример вывода
```
http://127.0.0.1:8005/secure
X-Frame-Options: OK
X-Content-Type-Options: OK
Content-Security-Policy: OK
Referrer-Policy: OK

http://127.0.0.1:8005/weak
X-Frame-Options: MISSING
X-Content-Type-Options: OK
Content-Security-Policy: MISSING
Referrer-Policy: MISSING

http://127.0.0.1:8005/nope
Skipped: status 404

http://127.0.0.1:1
Error: cannot connect
```

## Как это работает
1. Скрипт берёт URL из аргументов командной строки и для каждого делает GET-запрос через `requests` с таймаутом 5 секунд.
2. Если ответ не 200, заголовки не проверяются, и выводится `Skipped: status <код>`. Редиректы `requests` проходит сам, поэтому проверяется итоговая страница.
3. Для ответа 200 скрипт проверяет наличие каждого заголовка из списка (имена сравниваются без учёта регистра) и выводит `OK` или `MISSING`. Значение заголовка не проверяется, только его наличие.
4. Ошибки соединения (сервер недоступен, таймаут, неверный адрес) не прерывают работу: для такого URL выводится `Error: cannot connect`, и скрипт переходит к следующему.
