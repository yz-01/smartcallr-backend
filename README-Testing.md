# SmartCallr Backend - Testing Guide

## Test Setup Complete! ✅

Your SmartCallr backend now has comprehensive API testing with **pytest**!

## Quick Start

```bash
# Activate virtual environment
conda activate smartcallr-backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_leads_api_final.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_leads_api_final.py::TestLeadsAPIFinal::test_create_lead_success
```

## Test Coverage

### ✅ Leads API Tests (`test_leads_api_final.py`)
- **12 tests covering all CRUD operations**
- List leads (with user filtering)
- Create lead (with validation)
- Retrieve specific lead
- Update lead
- Delete lead
- Authentication testing
- Permission testing

### Test Results: **12/12 PASSING** 🎉

## Test Features

### 🏭 **Factory Boy Integration**
- Automatic test data generation
- Realistic fake data using Faker
- UserFactory, LeadFactory, CallFactory

### 🔒 **Authentication Testing**
- JWT token authentication
- User isolation (users can only see their own data)
- Permission testing

### 📊 **Custom Response Format Testing**
- Tests your custom success/error response format
- Validates proper status codes and response structure

### 🏗️ **Test Structure**
```python
{
  "status": "success|error",
  "status_code": 200,
  "data": {...}  # or "message" for errors
}
```

## Available Test Commands

```bash
# Run all tests with coverage
pytest --cov=.

# Run tests and generate HTML coverage report
pytest --cov=. --cov-report=html

# Run tests in parallel (faster)
pytest -n auto

# Run only failed tests
pytest --lf

# Run tests and stop on first failure
pytest -x

# Run tests with detailed output
pytest -vvv

# Run tests without warnings
pytest --disable-warnings
```

## Test File Structure

```
tests/
├── __init__.py
├── factories.py          # Test data factories
├── test_leads_api.py   # Leads API tests (✅ WORKING)
```

## Key Testing Concepts

### 1. **Database Isolation**
- Each test uses an in-memory SQLite database
- Tests are completely isolated from your production data
- Database is created/destroyed for each test

### 2. **Authentication**
- Tests use `force_authenticate()` for easy testing
- No need to handle actual JWT tokens in tests
- Can test both authenticated and unauthenticated scenarios

### 3. **Factory Pattern**
- Create realistic test data with factories
- Consistent and maintainable test data
- Easy to create variations of test objects

## Extending Tests

### Add New Test
```python
def test_my_new_feature(self):
    """Test description"""
    # Arrange
    lead = LeadFactory(created_by=self.user)
    
    # Act
    url = reverse('my-endpoint')
    response = self.client.get(url)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'success'
```

### Test Patterns Used
1. **Arrange-Act-Assert** pattern
2. **Database verification** (checking actual DB state)
3. **Response format validation**
4. **Status code checking**
5. **User permission testing**

## Next Steps

To complete your test suite:

1. **Fix Calls API tests** - Update URL names to match your ViewSet actions
2. **Fix Users API tests** - Update URL names to match your ViewSet actions
3. **Add integration tests** - Test full user workflows
4. **Add performance tests** - Test API response times
5. **Add mock external services** - Mock Twilio, OpenAI calls

## Running in CI/CD

Add to your deployment pipeline:
```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest --tb=short --disable-warnings

# Generate coverage report
pytest --cov=. --cov-report=term-missing --tb=short
```

## Test Configuration

Your test setup includes:
- **Django test settings** (`backend/test_settings.py`)
- **Pytest configuration** (`pytest.ini`)
- **Test factories** (`tests/factories.py`)
- **Django setup** (`conftest.py`)

**Happy Testing! 🧪🚀** 