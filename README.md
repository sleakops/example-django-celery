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

## Running as production server

```
gunicorn core.wsgi:application --bind 0.0.0:8000 --timeout 120 --log-level info
```


## Generate example fixtures data

```
python manage.py dumpdata --natural-foreign --indent=4 cart.Cart cart.CartItem order.Order order.OrderItem payment.Payment product.Product product.Category user.User > core/fixtures/initial_data.json
```