# SmartCallr Backend - Testing Guide

Simple API testing with pytest.

## Quick Start

```bash
# Activate environment
conda activate smartcallr-backend

# Run all tests
pytest

# Run specific tests
pytest tests/test_leads_api.py -v
```

## Test Results

✅ **12/12 tests passing** - Leads API fully tested

## What's Tested

- **Lead CRUD operations** - Create, read, update, delete
- **Authentication** - User login/logout protection
- **Permissions** - Users only see their own data
- **Validation** - Invalid data handling
- **Error responses** - Proper error messages

## Test Commands

```bash
# Basic testing
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -x                 # Stop on first failure

# Specific tests
pytest tests/test_leads_api.py                # Test specific file
pytest -k "test_create"                       # Test specific pattern

# With coverage
pytest --cov=.                                # Show coverage
```

## Test Files

```
tests/
├── factories.py          # Test data generation
├── test_leads_api.py     # ✅ Leads API tests (12 tests)
└── conftest.py           # Test configuration
```

## Adding New Tests

```python
def test_my_feature(self):
    """Test description"""
    # Create test data
    lead = LeadFactory(created_by=self.user)
    
    # Make API call
    url = reverse('my-endpoint')
    response = self.client.get(url)
    
    # Check results
    assert response.status_code == 200
    assert response.data['status'] == 'success'
```

## Test Features

- **Fast** - In-memory database for speed
- **Isolated** - Each test runs independently
- **Realistic data** - Auto-generated test data with Faker
- **Custom responses** - Tests your actual response format

## Notes

- Tests use in-memory SQLite (not your real database)
- Test data is automatically created and cleaned up
- Authentication is mocked for easy testing
- All tests verify your custom response format
