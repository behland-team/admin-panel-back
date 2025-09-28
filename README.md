create venv: python3 -m venv venv
active venv: source ./venv/bin/activate
install django: pip install Django
show packages: pip freeze
add packages to requirements.txt: pip freeze > requirements.txt >> pip install -r requirements.txt

========
create django project => django-admin startproject admin_panel
create django app=>
python3 manage.py makemigrations
python3 manage.py migrate

create superuser:
python manage.py createsuperuser
