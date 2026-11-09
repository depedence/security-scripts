# SSH brute-force detector

Что делает: ищет и выводит айпишники, которые пытаются перебрать пароль для входа (>= 3 попыток и затем успешный вход). Сохраняет результат работы в reports.txt

## Запуск
uv run python src/ssh_bruteforce_detector/detect.py data/auth_sample.txt 3

## Пример вывода
198.51.100.7: 5
