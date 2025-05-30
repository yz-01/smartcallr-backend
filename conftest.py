import pytest
import os
import django
from django.conf import settings

# Set Django settings module for pytest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.test_settings')

# Setup Django
django.setup()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass
