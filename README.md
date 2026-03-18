# Django Example Project

A production-ready Django application with Celery task queue, Flower monitoring, PostgreSQL database, and RabbitMQ message broker.

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Run the Project

```bash
# Clone the repository
git clone <repository-url>
cd django-example

# Start all services
docker compose up -d

# Wait for services to initialize (about 30-45 seconds)
docker compose ps

# View logs
docker compose logs -f
```

### Access the Services

| Service | URL | Description |
|---------|-----|-------------|
| Django App | http://localhost:8000 | Main application |
| Django Admin | http://localhost:8000/admin/ | Admin panel (credentials: admin/admin) |
| Flower (Celery Monitor) | http://localhost:5555 | Task queue monitoring |
| RabbitMQ Management | http://localhost:15672 | Message broker UI (guest/guest) |

## 📁 Project Structure

```
.
├── core/                       # Main Django application
│   ├── settings/              # Environment-specific settings
│   │   ├── base.py           # Base configuration
│   │   ├── local.py          # Local development settings
│   │   └── production.py     # Production settings
│   ├── celery.py             # Celery configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI entry point
├── apps/                      # Django apps
│   └── users/                # User management
├── requirements/              # Python dependencies
│   ├── base.txt              # Core dependencies
│   ├── local.txt             # Development extras
│   └── production.txt        # Production extras
├── docker-entrypoint.sh       # Container startup script
├── Dockerfile                 # Main application image
├── Dockerfile.flower          # Flower monitoring image
├── docker-compose.yml         # Service orchestration
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔧 Services Overview

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **core** | django-example/core | 8000 | Django web application |
| **celeryworker** | django-example/core | - | Background task worker |
| **flower** | django-example/flower | 5555 | Celery monitoring UI |
| **db** | postgres:14 | 5432 | PostgreSQL database |
| **broker** | rabbitmq:3-management | 5672, 15672 | RabbitMQ message broker |

## 🛠️ Development

### Run Migrations

```bash
docker compose exec core python manage.py migrate
```

### Create Superuser

```bash
docker compose exec core python manage.py createsuperuser
```

### Run Tests

```bash
docker compose exec core python manage.py test
```

### Execute Management Commands

```bash
# Any Django management command
docker compose exec core python manage.py <command>

# Examples
docker compose exec core python manage.py shell
docker compose exec core python manage.py collectstatic
docker compose exec core python manage.py makemigrations
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f core
docker compose logs -f celeryworker
docker compose logs -f flower
docker compose logs -f db
docker compose logs -f broker
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart core
docker compose restart celeryworker
```

## 🔐 Environment Variables

Key environment variables (defined in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | auto-generated | Django secret key |
| `DJANGO_DEBUG` | True | Debug mode (False in production) |
| `DJANGO_SETTINGS_MODULE` | core.settings.local | Settings module |
| `DB_NAME` | postgres | Database name |
| `DB_USER` | postgres | Database user |
| `DB_PASSWORD` | qwerty123 | Database password |
| `DB_HOST` | db | Database host |
| `DB_PORT` | 5432 | Database port |
| `CELERY_BROKER_URL` | amqp://admin:admin@broker:5672/vhost | RabbitMQ connection |
| `CELERY_RESULT_BACKEND` | django-db | Task result storage |

## 🏗️ Building Images

### Build All Images

```bash
docker compose build
```

### Build Specific Image

```bash
# Main application
docker build --build-arg ENVIRONMENT=local -t django-example/core:latest .

# Flower monitoring
docker build --build-arg ENVIRONMENT=local -f Dockerfile.flower -t django-example/flower:latest .
```

### Build for Production

```bash
docker build --build-arg ENVIRONMENT=production -t django-example/core:prod .
```

## 🧹 Cleanup

```bash
# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes database data)
docker compose down -v

# Remove all images
docker compose down --rmi all

# Clean up unused Docker resources
docker system prune -f
```

## 🐛 Troubleshooting

### Services not starting

```bash
# Check service status
docker compose ps

# View detailed logs
docker compose logs <service-name>

# Check for port conflicts
docker ps
```

### Database connection issues

```bash
# Ensure database is healthy
docker compose ps db

# Check database logs
docker compose logs db

# Restart database
docker compose restart db
```

### Celery worker not processing tasks

```bash
# Check worker status
docker compose logs celeryworker

# Restart worker
docker compose restart celeryworker

# Check Flower for task status
open http://localhost:5555
```

### Port already in use

If you see "port is already allocated" errors, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

## 📦 Dependencies

### Python Packages

Core dependencies are managed through `requirements/`:

- **base.txt**: Django, Celery, psycopg2, gunicorn
- **local.txt**: Debug toolbar, development tools
- **production.txt**: Production optimizations

### Add New Dependencies

```bash
# Add to appropriate requirements file
echo "package-name==version" >> requirements/base.txt

# Rebuild images
docker compose build
```

## 🚀 Production Deployment

### Environment Setup

1. Update `.env` with production values:
   ```
   ENVIRONMENT=production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<strong-secret-key>
   ```

2. Build production images:
   ```bash
   docker build --build-arg ENVIRONMENT=production -t django-example/core:prod .
   ```

3. Run with production settings:
   ```bash
   docker compose -f docker-compose.yml up -d
   ```

### AWS Managed Services

This project can leverage AWS managed services for production:

| Component | AWS Service |
|-----------|-------------|
| PostgreSQL | Amazon RDS |
| RabbitMQ | Amazon MQ |
| Cache (if added) | Amazon ElastiCache |
| File Storage | Amazon S3 |

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Flower Documentation](https://flower.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## 📝 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Note**: This project is configured for local development by default. Always review and update security settings before deploying to production.
