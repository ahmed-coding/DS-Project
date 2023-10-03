#!/usr/bin/env sh

echo 'Apply database mogrations'

python manage.py migrate

echo 'Apply collectstatic'

# python manage.py collectstatic -yes

# echo 'Apply spectacular schema'

# python manage.py spectacular --color --file schema.yml

exec "$@"
