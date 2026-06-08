# Django Example Project

A complete Django web application with Celery task processing, PostgreSQL database, RabbitMQ message broker, and Flower monitoring.

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd django-example
```

### 2. Environment Configuration

Create your `.env` file from the provided template:

```bash
cp .env.local .env
```

The `.env` file contains all necessary configuration. Default values are pre-configured for local development.

### 3. Build and Start Services

```bash
docker compose up -d
```

This will start all services:
- **PostgreSQL** database (port 5432)
- **RabbitMQ** message broker (ports 5672, 15672)
- **Django** web application (port 8000)
- **Celery** worker
- **Flower** monitoring UI (port 5555)

### 4. Verify Services

Check service status:
```bash
docker compose ps
```

View logs:
```bash
docker compose logs -f
```

### 5. Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| Django App | http://localhost:8000 | Main web application |
| Django Admin | http://localhost:8000/admin/ | Admin panel |
| Flower UI | http://localhost:5555 | Celery task monitoring |
| RabbitMQ UI | http://localhost:15672 | Message broker management |

**Default RabbitMQ credentials:**
- Username: `admin`
- Password: `admin`

## 📁 Project Structure

```
.
├── apps/                       # Django applications
│   ├── base/                   # Base app with shared utilities
│   ├── client/                 # Client management app
│   ├── post/                   # Post/content app
│   └── user/                   # User management app
├── core/                       # Django project configuration
│   ├── settings/               # Environment-specific settings
│   │   ├── base.py            # Base configuration
│   │   ├── local.py           # Local development settings
│   │   └── production.py      # Production settings
│   ├── celery.py              # Celery configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
├── requirements/               # Python dependencies
│   ├── _base.txt             # Base dependencies
│   ├── local.txt             # Local development extras
│   ├── production.txt        # Production extras
│   └── test.txt              # Test dependencies
├── Dockerfile                # Main Django service image
├── Dockerfile.celeryworker    # Celery worker image
├── Dockerfile.flower          # Flower monitoring image
├── docker-compose.yml         # Service orchestration
├── docker-entrypoint.sh       # Container startup script
├── .env.local                 # Environment template
└── README.md                  # This file
```

## 🔧 Development

### Running Management Commands

```bash
# Create superuser
docker compose exec core python manage.py createsuperuser

# Run migrations manually
docker compose exec core python manage.py migrate

# Django shell
docker compose exec core python manage.py shell

# Check logs for a specific service
docker compose logs -f core
```

### Database Migrations

Migrations run automatically on container startup. To create new migrations:

```bash
docker compose exec core python manage.py makemigrations
```

### Static Files

In local development, static files are served automatically. For production:

```bash
docker compose exec core python manage.py collectstatic
```

## 🧪 Testing

```bash
# Run Django tests
docker compose exec core python manage.py test

# Run tests with coverage
docker compose exec core python manage.py test --verbosity=2
```

## 🛑 Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes database data)
docker compose down -v
```

## 🔐 Environment Variables

Key environment variables (defined in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django security key | Auto-generated |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_SETTINGS_MODULE` | Settings module path | `core.settings.local` |
| `DB_NAME` | PostgreSQL database name | `postgres` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `qwerty123` |
| `DB_HOST` | PostgreSQL host | `db` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `CELERY_BROKER_URL` | RabbitMQ connection URL | `amqp://admin:admin@broker:5672/vhost` |
| `CELERY_RESULT_BACKEND` | Celery result storage | `django-db` |

See `.env.local` for the complete list.

## 🏗️ Production Deployment

### Build Production Images

```bash
docker compose build --build-arg ENVIRONMENT=production
```

### Production Configuration

1. Update `.env` with production values:
   - Set `ENVIRONMENT=production`
   - Set `DJANGO_DEBUG=False`
   - Generate a secure `DJANGO_SECRET_KEY`
   - Configure `DJANGO_ALLOWED_HOSTS`
   - Set up AWS credentials for S3 storage

2. Use a production-grade database (AWS RDS, etc.)

3. Configure SSL/TLS certificates

4. Set up a reverse proxy (nginx, traefik)

### AWS Managed Services

This application can leverage AWS managed services:

| Component | AWS Service |
|-----------|-------------|
| PostgreSQL | Amazon RDS for PostgreSQL |
| RabbitMQ | Amazon MQ (RabbitMQ engine) or Amazon SQS |
| Static/Media Files | Amazon S3 |
| Email | Amazon SES |
| Cache | Amazon ElastiCache for Redis |

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check for port conflicts
docker ps

# View detailed logs
docker compose logs <service-name>

# Restart a specific service
docker compose restart <service-name>
```

### Database Connection Issues

```bash
# Check if database is healthy
docker compose ps db

# View database logs
docker compose logs db
```

### Celery Tasks Not Processing

```bash
# Check Celery worker logs
docker compose logs celeryworker

# Check Flower UI for task status
# http://localhost:5555

# Restart Celery worker
docker compose restart celeryworker
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Flower Documentation](https://flower.readthedocs.io/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy Coding! 🎉**
