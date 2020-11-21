@echo off
pipenv run celery -A interface worker --pool=solo -l INFO -E
pause