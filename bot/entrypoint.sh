#!/bin/sh
pwd
pip install -r requirements.txt
python manage.py migrate
python manage.py add_text
# При первом запуске создат пользователя админа
./manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@admin.com', 'admin', 'admin')"

gunicorn -c "/srv/www/bot/gunicorn_config.py" bot.wsgi
