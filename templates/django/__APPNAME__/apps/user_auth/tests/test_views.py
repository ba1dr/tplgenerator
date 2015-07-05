import pytest

from utils.decorators import authenticated_redirect


class DescribeLogin:
    """Test the login view"""
    def it_loads_login(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def it_redirects_to_dashboard_if_logged_in(self, admin_client):
        response = admin_client.get('/login', follow=True)
        assert response.redirect_chain[0][0].endswith('/login/')
        assert response.redirect_chain[1][0].endswith('/dashboard')

class DescribeLogout:
    """Test the logout view"""
    def it_doesnt_load_with_get_request(self, admin_client):
        response = admin_client.get('/logout/')
        assert response.status_code == 405

    def it_allows_post(self, admin_client):
        response = admin_client.post('/logout/', {})
        assert response.url == 'http://testserver/'
