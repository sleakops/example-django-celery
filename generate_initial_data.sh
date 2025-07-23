#!/usr/bin/env bash

# bash options

set -o errexit
set -o nounset

# python manage.py shell -c "from apps.user.models import User; user = User.objects.create(username='admin', is_staff=True, is_superuser=True); user.set_password('admin'); user.save()"
python manage.py loaddata core/fixtures/initial_data.json
