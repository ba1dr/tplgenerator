
from django import template

register = template.Library()


@register.filter
def commajoin(lll):
    return ", ".join(lll)

