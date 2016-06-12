
from django.conf import settings


def common_context(request):
    context = {}
    context['my_company_name'] = "My Company"
    return context
