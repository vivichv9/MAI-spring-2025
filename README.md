# MAI-spring-2025
Command project of MAI python course. Spring 2025


### Запуск инфры:
При первом запуске - `./setup.sh`
Второй и последующие - `docker compose up -d`


### Генерация  данных

Создать виртульаное окружение(при первом заупске)
```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```


Запустить скрипт генерации данных:
`python ./scripts/data_generation.py`

