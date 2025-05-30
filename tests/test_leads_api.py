import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from leads.models import Lead
from tests.factories import UserFactory, LeadFactory


@pytest.mark.django_db
class TestLeadsAPIFinal:

    def setup_method(self):
        """Set up test data for each test method"""
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_leads_success(self):
        """Test successful retrieval of leads list"""
        # Create test leads
        leads = LeadFactory.create_batch(3, created_by=self.user)

        url = reverse('leads-list-leads')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert len(response.data['data']) == 3

    def test_list_leads_unauthenticated(self):
        """Test that unauthenticated requests are rejected"""
        self.client.force_authenticate(user=None)

        url = reverse('leads-list-leads')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_lead_success(self):
        """Test successful lead creation"""
        lead_data = {
            'name': 'John Doe',
            'phone': '+1234567890',
            'email': 'john@example.com'
        }

        url = reverse('leads-create-lead')
        response = self.client.post(url, lead_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'success'
        assert response.data['data']['name'] == lead_data['name']
        assert response.data['data']['phone'] == lead_data['phone']
        assert response.data['data']['email'] == lead_data['email']

        # Verify lead was created in database
        lead = Lead.objects.get(id=response.data['data']['id'])
        assert lead.created_by == self.user

    def test_create_lead_invalid_data(self):
        """Test lead creation with invalid data"""
        invalid_data = {
            'name': '',  # Empty name should fail validation
            'phone': 'invalid-phone',
            'email': 'invalid-email'
        }

        url = reverse('leads-create-lead')
        response = self.client.post(url, invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'

    def test_retrieve_lead_success(self):
        """Test successful retrieval of a specific lead"""
        lead = LeadFactory(created_by=self.user)

        url = reverse('leads-get-lead', kwargs={'pk': lead.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['data']['id'] == lead.id
        assert response.data['data']['name'] == lead.name

    def test_retrieve_nonexistent_lead(self):
        """Test retrieval of a non-existent lead"""
        url = reverse('leads-get-lead', kwargs={'pk': 999})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'

    def test_update_lead_success(self):
        """Test successful lead update"""
        lead = LeadFactory(created_by=self.user)
        update_data = {
            'name': 'Updated Name',
            'phone': lead.phone,
            'email': lead.email
        }

        url = reverse('leads-update-lead', kwargs={'pk': lead.id})
        response = self.client.put(url, update_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['data']['name'] == update_data['name']

        # Verify update in database
        lead.refresh_from_db()
        assert lead.name == update_data['name']

    def test_delete_lead_success(self):
        """Test successful lead deletion"""
        lead = LeadFactory(created_by=self.user)

        url = reverse('leads-delete-lead', kwargs={'pk': lead.id})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['status'] == 'success'

        # Verify deletion in database
        assert not Lead.objects.filter(id=lead.id).exists()

    def test_access_other_user_lead(self):
        """Test that users cannot access leads created by other users"""
        other_user = UserFactory()
        lead = LeadFactory(created_by=other_user)

        url = reverse('leads-get-lead', kwargs={'pk': lead.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'

    def test_list_leads_filters_by_user(self):
        """Test that list only returns current user's leads"""
        other_user = UserFactory()

        # Create leads for both users
        my_leads = LeadFactory.create_batch(2, created_by=self.user)
        other_leads = LeadFactory.create_batch(3, created_by=other_user)

        url = reverse('leads-list-leads')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        # Should only return current user's leads
        assert len(response.data['data']) == 2

        # Verify all returned leads belong to current user
        for lead_data in response.data['data']:
            lead = Lead.objects.get(id=lead_data['id'])
            assert lead.created_by == self.user

    def test_create_lead_with_minimal_data(self):
        """Test creating lead with only required fields"""
        lead_data = {
            'name': 'Minimal Lead',
            'phone': '+1234567890',
            'email': 'minimal@example.com'
        }

        url = reverse('leads-create-lead')
        response = self.client.post(url, lead_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'success'
        assert response.data['data']['name'] == lead_data['name']

    def test_update_lead_partial_data(self):
        """Test updating lead with partial data"""
        lead = LeadFactory(created_by=self.user)

        # Only update name, keep phone and email same
        update_data = {
            'name': 'Partially Updated',
            'phone': lead.phone,
            'email': lead.email
        }

        url = reverse('leads-update-lead', kwargs={'pk': lead.id})
        response = self.client.put(url, update_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert response.data['data']['name'] == 'Partially Updated'
        assert response.data['data']['phone'] == lead.phone
        assert response.data['data']['email'] == lead.email
