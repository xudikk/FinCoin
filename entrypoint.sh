#set -o errexit
#set -o pipefail
#set -o nounset

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8060
#gunicorn config.wsgi:application --bind 0.0.0.0:8050
