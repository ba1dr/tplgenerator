
from django.views.generic import TemplateView

from utils.views import ViewMixin


class HomeView(ViewMixin, TemplateView):
    template_name = 'dashboards/home.html'
    page_title = 'Dashboard'


class DashboardView(ViewMixin, TemplateView):
    template_name = 'dashboards/dashboard.html'
    page_title = 'Dashboard'
