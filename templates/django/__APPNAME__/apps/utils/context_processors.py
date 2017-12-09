
from django.conf import settings


def common_context(request):
    context = {}
    context['theme_name'] = request.session.get('theme_name') or 'default'
    context['my_company_name'] = settings.COMPANY_NAME
    return context
