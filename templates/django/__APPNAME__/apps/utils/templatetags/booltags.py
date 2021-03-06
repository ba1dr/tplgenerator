
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# @register.simple_tag(is_safe=True)
@register.filter(needs_autoescape=False)
def bool2html(value):
    if value:
        return mark_safe('<span class="fa fa-check text-success"></span>')
    return mark_safe('<span class="fa fa-times text-danger"></span>')
