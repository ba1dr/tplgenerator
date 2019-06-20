
from django.conf import settings


def common_context(request):
    context = {}
    context['theme_name'] = request.session.get('theme_name') or 'default'
    context['my_company_name'] = settings.COMPANY_NAME
    wsproto = 'ws'
    if request.scheme == 'https':
        wsproto = 'wss'
    wshost = request.get_host()
    context['wsurl'] = f"{wsproto}://{wshost}/ws/"
    return context
