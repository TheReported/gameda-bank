project_name := `basename $(dirname $(realpath $0))`

migrate app="":
    python manage.py migrate {{ app }}

runserver:
    python manage.py runserver

startapp app:
    python manage.py startapp {{ app }}

makemigrations app="":
    python manage.py makemigrations {{ app }}

shell:
    python manage.py shell

check:
    python manage.py check

clean:
    #!/usr/bin/env bash
    find . -name '__pycache__' -not -path "./.venv/*" -prune -exec rm -rf {} \;
    find . -name '*.pyc' -not -path "./.venv/*" -exec rm {} \;
    find . -name '.DS_Store' -not -path "./.venv/*" -exec rm {} \;
    rm -rf .mypy_cache

zip: clean
    #!/usr/bin/env bash
    rm -f {{ project_name }}.zip
    zip -r {{ project_name }}.zip . -x .venv/**\*

dockup:
    docker compose up

dockdown:
    docker compose down
