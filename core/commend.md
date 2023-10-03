[Documentation]
python manage.py spectacular --color --file schema.yml

[staticfile]
python manage.py collectstatic

[Docker]
docker-compose up -d --build
docker exec -it containerName /bin/sh
