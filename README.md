# example-django-celery

Complete Django + Celery example with RabbitMQ broker for asynchronous task processing.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Make utility

### Running the Project

1. Copy environment file:
   ```bash
   cp .env.local .env
   ```

2. Start all services (Django, PostgreSQL, RabbitMQ, Celery Worker, Flower):
   ```bash
   make run
   ```
   This will build images on first run and start:
   - **Django app**: `http://localhost:8000`
   - **PostgreSQL**: Database on port `5432`
   - **RabbitMQ**: Broker on port `5672` (Management UI: `http://localhost:15672`)
   - **Celery Worker**: Background task processor
   - **Flower**: Task monitoring dashboard at `http://localhost:5555`

3. Create superuser to access Django admin:
   ```bash
   make createsuperuser
   ```

4. Access the application:
   - **Django Admin**: http://localhost:8000/admin/
   - **Flower Dashboard**: http://localhost:5555

### Available Make Commands

Run `make help` to see all available commands:
- `make run` - Start all services
- `make stop` - Stop all containers
- `make bash` - Access bash inside core container
- `make shell` - Access Django shell
- `make migrate` - Run database migrations
- `make makemigrations` - Create new migrations
- `make reset-db` - Reset database (⚠️ deletes all data)
- `make rebuild-core` - Rebuild core container from scratch
- `make rebuild-all` - Rebuild everything

## Project Structure

```
├── apps/
│   ├── client/          # Client app
│   │   ├── tasks.py     # Celery tasks definitions
│   │   ├── admin.py     # Admin actions that trigger tasks
│   │   └── views.py     # Views (can trigger tasks)
│   ├── post/            # Post app
│   └── user/            # User app
├── core/
│   ├── celery.py        # Celery configuration
│   └── settings/        # Django settings
├── docker-compose.yml   # All services orchestration
├── Makefile            # Helper commands
└── .env.local          # Environment variables template
```

---

## How to Install & Configure Celery (Step by Step)

If you want to add Celery to your own Django project, follow these steps:

### Step 1: Install Dependencies

Add to your `requirements/_base.txt` or `requirements.txt`:

```txt
celery==5.3.6                    # Core Celery library
django-celery-results==2.5.1     # Optional: Store results in DB
flower==2.0.1                    # Optional: Monitoring dashboard
```

**Install:**
```bash
pip install -r requirements.txt
```

### Step 2: Configure Django Settings

Add Celery configuration to `core/settings/base.py`:

```python
# Celery Configuration
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")  # RabbitMQ or Redis URL
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")  # Optional: "django-db" to store results
CELERY_WORKER_PREFETCH_MULTIPLIER = env.int("CELERY_WORKER_PREFETCH_MULTIPLIER", default=1)
CELERY_RESULT_EXTENDED = env.bool("CELERY_RESULT_EXTENDED", default=False)  # Optional: Extended result info
```

**Important notes:**
- `CELERY_RESULT_BACKEND` and `CELERY_RESULT_EXTENDED` are **optional** - only needed if you want to store task results in the database
- If using `django-celery-results`, add `"django_celery_results"` to `INSTALLED_APPS`

Reference: [`core/settings/base.py:138-143`](https://github.com/sleakops/example-django-celery/blob/main/core/settings/base.py#L138)

### Step 3: Create Celery App

Create `core/celery.py`:

```python
import os
from celery import Celery
from django.conf import settings

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

# Create Celery app
app = Celery("core")

# Load config from Django settings with CELERY_ namespace
app.config_from_object(settings, namespace="CELERY")

# Auto-discover tasks.py in all Django apps
app.autodiscover_tasks()
```

Reference: [`core/celery.py`](https://github.com/sleakops/example-django-celery/blob/main/core/celery.py)

### Step 4: Initialize Celery on Django Startup

Modify `core/__init__.py` to import Celery app:

```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### Step 5: Define Tasks

Create `tasks.py` in any Django app (e.g., `apps/client/tasks.py`):

```python
from celery import shared_task

@shared_task
def my_async_task(param):
    # Your task logic here
    print(f"Processing: {param}")
    return "Task completed"
```

**Magic:** Celery automatically discovers any `tasks.py` file in your Django apps!

Reference: [`apps/client/tasks.py`](https://github.com/sleakops/example-django-celery/blob/main/apps/client/tasks.py)

### Step 6: Set Environment Variables

Add to your `.env` file:

```bash
# Celery Configuration
CELERY_BROKER_URL=amqp://admin:admin@broker:5672/vhost  # RabbitMQ
# OR
# CELERY_BROKER_URL=redis://localhost:6379/0  # Redis

CELERY_RESULT_BACKEND=django-db  # Optional: Store results in database
```

### Step 7: Run Celery Worker

```bash
# Development
celery -A core.celery worker -l INFO

# Production (with more options)
celery -A core.celery worker -l INFO --concurrency 4 --max-tasks-per-child 100
```

**In Docker (see `docker-compose.yml:53-70`):**
```yaml
celeryworker:
  image: django-example/core
  command: celery -A core.celery worker -l INFO --concurrency 1
  depends_on:
    - db
    - broker
```

### Step 8: Trigger Tasks

From anywhere in your Django code:

```python
from apps.client.tasks import my_async_task

# Asynchronous execution (non-blocking)
task = my_async_task.delay("parameter")
print(f"Task ID: {task.id}")

# With custom options
task = my_async_task.apply_async(
    args=["parameter"],
    countdown=10,  # Execute after 10 seconds
)
```

---

## Celery Architecture

This project demonstrates the complete Celery workflow for asynchronous task processing:

```
Django View/Admin → Celery Task (.delay) → RabbitMQ Broker → Celery Worker → Result Backend (DB)
```

### Components

#### 1. **Broker (RabbitMQ)** 
Message broker that queues tasks between Django and workers.

- **Configuration** (`.env.local`):
  ```bash
  CELERY_BROKER_URL=amqp://admin:admin@broker:5672/vhost
  ```
- **Docker service** (`docker-compose.yml:20-30`): RabbitMQ with management plugin
- **Ports**: 
  - `5672` - AMQP protocol
  - `15672` - Management UI (http://localhost:15672, user: `admin`, pass: `admin`)

#### 2. **Celery App** (`core/celery.py`)
Main Celery application configuration.

```python
app = Celery("core")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()  # Finds tasks.py in all Django apps
```

- Auto-discovers tasks in `tasks.py` from all registered Django apps
- Loaded on Django startup via `core/__init__.py:3`
- Namespace `CELERY_` means all config uses this prefix in `.env`

#### 3. **Tasks** (`apps/client/tasks.py`)
Asynchronous task definitions using `@shared_task` decorator.

**Example task** (`apps/client/tasks.py:7-17`):
```python
@shared_task
def collect_post_by_client(client_id):
    client = Client.objects.get(id=client_id)
    print(f'Request: {client.username}')
    
    for i in range(1, 200):
        Post.objects.create(
            client=client,
            source="twitter",
            description=f"Lorem {i}"
        )
```

This task creates 200 posts asynchronously, preventing request timeout.

#### 4. **Result Backend**
Stores task results and status in database.

- **Configuration** (`.env.local:23`):
  ```bash
  CELERY_RESULT_BACKEND="django-db"
  ```
- **Package**: `django-celery-results` (installed in `requirements.txt:6`)
- **Purpose**: Track task status (PENDING, STARTED, SUCCESS, FAILURE) and retrieve results

#### 5. **Celery Worker** (`docker-compose.yml:53-70`)
Background process that executes tasks from the queue.

```yaml
celeryworker:
  command: celery -A core.celery worker -l INFO --concurrency 1
```

- Runs in separate Docker container
- Shares same codebase as Django app
- Configuration:
  - `--concurrency 1`: Process 1 task at a time
  - `--max-tasks-per-child 1`: Restart worker after each task (prevents memory leaks)
  - `--prefetch-multiplier 1`: Don't prefetch tasks

#### 6. **Flower** (`docker-compose.yml:72-87`)
Real-time monitoring dashboard for Celery.

```yaml
flower:
  command: celery -A core.celery flower
  ports:
    - "5555:5555"
```

- **Access**: http://localhost:5555
- **Features**: Monitor tasks, workers, queue status, task history, and execution times

---

## How to Trigger Tasks

### Option 1: From Django Admin (Already Implemented)

The project includes a Django admin action in `apps/client/admin.py:10-19`:

```python
@admin.action(description="Run collect post task")
def collect_post(modeladmin, request, queryset):
    for c in queryset.all():
        collect_post_by_client.delay(c.id)  # Sends task to broker
        messages.add_message(
            request,
            messages.INFO,
            f"Run collect post task for client {c.username}",
        )
```

**Usage Steps:**
1. Go to http://localhost:8000/admin/client/client/
2. Select one or more clients from the list
3. Choose **"Run collect post task"** from the actions dropdown
4. Click "Go"
5. The task is sent to RabbitMQ and processed by Celery worker
6. Monitor progress in Flower: http://localhost:5555

### Option 2: From a Django View (Code Example)

You can trigger tasks from any Django view. Here's a complete example:

```python
# apps/client/views.py
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import collect_post_by_client

def trigger_collect_posts(request, client_id):
    """Trigger async task to collect posts for a client"""
    task = collect_post_by_client.delay(client_id)
    return JsonResponse({
        'task_id': task.id,
        'status': 'Task sent to broker',
        'client_id': client_id,
        'monitor_url': f'http://localhost:5555/task/{task.id}'
    })

def check_task_status(request, task_id):
    """Check the status of a running task"""
    task = AsyncResult(task_id)
    
    response_data = {
        'task_id': task_id,
        'status': task.status,  # PENDING, STARTED, SUCCESS, FAILURE, RETRY
        'ready': task.ready(),
    }
    
    if task.ready():
        if task.successful():
            response_data['result'] = task.result
        else:
            response_data['error'] = str(task.info)
    
    return JsonResponse(response_data)
```

**Add to `core/urls.py`:**

```python
from django.urls import path
from apps.client import views

urlpatterns = [
    # ... existing patterns
    path('api/collect-posts/<int:client_id>/', views.trigger_collect_posts, name='trigger_collect_posts'),
    path('api/task-status/<str:task_id>/', views.check_task_status, name='check_task_status'),
]
```

**Usage:**
```bash
# Trigger task
curl http://localhost:8000/api/collect-posts/1/

# Response:
# {
#   "task_id": "a7f3e0b2-5c8d-4e9f-b1a2-3d4e5f6a7b8c",
#   "status": "Task sent to broker",
#   "client_id": 1,
#   "monitor_url": "http://localhost:5555/task/a7f3e0b2-5c8d-4e9f-b1a2-3d4e5f6a7b8c"
# }

# Check task status
curl http://localhost:8000/api/task-status/a7f3e0b2-5c8d-4e9f-b1a2-3d4e5f6a7b8c/

# Response:
# {
#   "task_id": "a7f3e0b2-5c8d-4e9f-b1a2-3d4e5f6a7b8c",
#   "status": "SUCCESS",
#   "ready": true
# }
```

### Option 3: From Django Shell

```bash
make shell
```

```python
from apps.client.tasks import collect_post_by_client

# Trigger task
task = collect_post_by_client.delay(1)
print(f"Task ID: {task.id}")

# Check status
print(f"Status: {task.status}")

# Wait for result (blocking)
result = task.get(timeout=60)
```

---

## Complete Task Flow Example

Here's what happens when you trigger a task:

1. **User Action**: Admin selects a client and clicks "Run collect post task"
2. **Django**: Calls `collect_post_by_client.delay(client_id)` (non-blocking)
3. **Celery**: Serializes task (function name + arguments) and sends to RabbitMQ
4. **RabbitMQ**: Stores task message in queue
5. **Celery Worker**: Picks up task from queue and executes `collect_post_by_client()`
6. **Task Execution**: Creates 200 posts in PostgreSQL database
7. **Result Storage**: Saves task result/status in `django_celery_results` table
8. **Monitoring**: View real-time progress in Flower dashboard

**Timing**:
- Django response: ~50ms (immediately returns after queuing)
- Task execution: ~5-10 seconds (running in background)
- Database operations: 200 inserts

---

## Environment Configuration

Key Celery settings in `.env.local`:

```bash
# Celery Configuration
CELERY_RESULT_BACKEND="django-db"                          # Store results in PostgreSQL
CELERY_BROKER_URL=amqp://admin:admin@broker:5672/vhost    # RabbitMQ connection
CELERY_WORKER_CONCURRENCY=1                               # Number of worker processes
CELERY_WORKER_PREFETCH_MULTIPLIER=1                       # Tasks to prefetch per worker
CELERY_WORKER_MAX_TASKS_PER_CHILD=10                      # Restart worker after N tasks
```

---

## Monitoring & Debugging

### Flower Dashboard
Access http://localhost:5555 to:
- View active workers
- Monitor task queue
- Check task execution history
- See task success/failure rates
- Inspect individual task details

### RabbitMQ Management UI
Access http://localhost:15672 (user: `admin`, pass: `admin`) to:
- View message queues
- Check connection status
- Monitor message rates
- Inspect queue bindings

### Check Celery Worker Logs
```bash
docker logs django-example-celeryworker -f
```

### Check Django Logs
```bash
docker logs django-example-core -f
```

---

## Troubleshooting

**Workers not processing tasks?**
```bash
# Check worker status
docker ps | grep celeryworker

# Restart worker
docker restart django-example-celeryworker
```

**RabbitMQ connection issues?**
```bash
# Check broker is running
docker ps | grep broker

# Check environment variable
docker exec django-example-core env | grep CELERY_BROKER_URL
```

**Tasks stuck in PENDING?**
- Verify worker is running: `docker ps | grep celeryworker`
- Check worker logs: `docker logs django-example-celeryworker`
- Ensure broker URL is correct in `.env`

**Database errors in tasks?**
- Check PostgreSQL is running: `docker ps | grep db`
- Verify database migrations: `make migrate`

---

## Health Check

- **Port**: 8000
- **Path**: `/healthcheck/` (if implemented)
- **Expected Status**: 200
