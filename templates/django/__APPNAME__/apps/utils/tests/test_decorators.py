import pytest
import mock

from utils.decorators import authenticated_redirect


class DescribeAuthenticatedRedirect:
    """Test the authenticated_redirect decorator"""
    @classmethod
    def setup_class(cls):
        cls.request = mock.Mock()
        cls.request.path = '/login/'

    def it_works_without_kwargs(self):
        @authenticated_redirect
        def my_function(request):
            return True

        result = my_function(self.request)
        assert result.url == '/dashboard'

    def it_works_with_kwargs(self):
        @authenticated_redirect(path='home')
        def my_function(request):
            return True

        result = my_function(self.request)
        assert result.url == '/'

    def it_avoids_redirect_loop(self):
        @authenticated_redirect(path='login')
        def my_function(request):
            return True

        result = my_function(self.request)
        assert result.url == '/dashboard'
