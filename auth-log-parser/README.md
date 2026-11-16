# Auth log parser

Скрипт на Python, который разбирает лог SSH-авторизаций в структурированный
список событий, сохраняет его в `data/events.json` и выводит статистику:
сколько всего событий, сколько неудачных и успешных входов и с каких IP
было 2 и больше неудачных попыток.

## Запуск
```
python scripts/auth-log-parser/src/auth_log_parser/log_parser.py
```
Аргументов нет: пути к логу (`scripts/auth-log-parser/data/auth_small.txt`)
и к JSON (`scripts/auth-log-parser/data/events.json`) зашиты в коде, поэтому
скрипт запускается из папки, в которой лежит `scripts/`. Файл `events.json`
перезаписывается при каждом запуске.

## Что это находит
| Ситуация в логе | Как учитывается |
|---|---|
| Строка со словом `Failed` | событие `failed` |
| Любая другая строка с `from` | событие `accepted` |
| `Failed password for invalid user guest from ...` | `failed`, пользователь `guest` |
| 2 и больше неудачных попыток с одного IP | IP попадает в «Failed by IP» |
| 1 неудачная попытка с IP | считается в `Failed`, но в список IP не попадает |

## Пример данных
```
Nov  4 10:01:12 srv sshd[1201]: Failed password for root from 203.0.113.5 port 52114 ssh2
Nov  4 10:01:15 srv sshd[1201]: Failed password for root from 203.0.113.5 port 52115 ssh2
Nov  4 10:03:40 srv sshd[1207]: Accepted password for alex from 198.51.100.7 port 40322 ssh2
Nov  4 10:04:40 srv sshd[1210]: Failed password for invalid user guest from 192.0.2.44 port 22114 ssh2
```

## Пример вывода
```
Total events: 5
Failed: 4
Accepted: 1
Failed by IP:
203.0.113.5: 2
```
В `events.json` каждое событие записывается так:
```
{
  "time": "10:01:12",
  "result": "failed",
  "user": "root",
  "ip": "203.0.113.5"
}
```

## Как это работает
1. Скрипт читает лог построчно и делит строку через split(). Время это третье слово, IP слово сразу после `from`, пользователь слово сразу перед `from`.
2. Если в строке есть `Failed`, событие помечается как `failed`, иначе как `accepted`. Все события собираются в список и записываются в `data/events.json`.
3. Затем скрипт заново читает `events.json` и считает неудачные и успешные события, а неудачи дополнительно считает по IP в словаре.
4. В «Failed by IP» выводятся IP, у которых неудачных попыток не меньше 2. Порог задан в коде.
5. Проверок входных данных нет: строка без слова `from` или отсутствующий файл лога приводят к ошибке Python.
