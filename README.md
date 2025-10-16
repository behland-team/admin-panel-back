create venv: python3 -m venv venv
active venv: source ./venv/bin/activate
install django: pip install Django
show packages: pip freeze
add packages to requirements.txt: pip freeze > requirements.txt >> pip install -r requirements.txt

========
create django project => django-admin startproject admin_panel
create django app=>python3 manage.py startapp <app_name>

create superuser:
python manage.py createsuperuser

=========
python3 manage.py makemigrations --settings=admin_panel.settings.dev
python3 manage.py migrate --settings=admin_panel.settings.dev
python3 manage.py runserver --settings=admin_panel.settings.dev
