## Makefile helpers

The Makefile contains a few helpers to make your life easier. Run `make help` to know more.


## Running

1. Copy file `.env.local` to `.env`
2. Run command `make run` to run the project (the first time run build images)
3. Create super user to access django admin http://localhost:8000/admin/ by command `make createsuperuser`


## Places you'll need to visit

- Backend Core admin app: http://localhost:8000/admin/
- Celery monitoring: http://localhost:5555


## Config health check

port: 8000
path: /healthcheck/
status code: 200

## Running as development server

```
python manage.py runserver 0.0.0:8000
```


## Environment variables para demo

```
DJANGO_ADMIN_URL=admin/
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=s8s6s5t2nu00
DJANGO_SETTINGS_MODULE=core.settings.production
ENVIRONMENT=production
ADMIN_ENABLED=True
```


## Running as production server

```
gunicorn core.wsgi:application --bind 0.0.0:8000 --timeout 120 --log-level info
```


## Commandos para hooks


Run db migrations: 

```
python manage.py migrate --no-input
```


Collect static files:

```
python manage.py collectstatic --no-input
```


## Comando para levantar data de demo 

```
sh ./generate_initial_data.sh
```


## Para configurar Celery 

Tiene como dependencia RabbitMQ, y se debe configurar las variables de entorno `CELERY_ENABLED` y `CELERY_BROKER_URL`.

```
celery -A core.celery worker -l INFO --concurrency 1 --max-tasks-per-child 1 --prefetch-multiplier 1 -n celery@%h
```


## Para configurar el bucket de s3

Se necesita la variable de entorno `DJANGO_AWS_STORAGE_BUCKET_NAME` y `DJANGO_AWS_STORAGE_ENABLED`



## Generate example fixtures data

```
python manage.py dumpdata --natural-foreign --indent=4 cart.Cart cart.CartItem order.Order order.OrderItem payment.Payment product.Product product.Category user.User > core/fixtures/initial_data.json
```

