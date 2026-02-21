import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_json(value):
    try:
        return mark_safe(json.dumps(value))
    except Exception:
        return mark_safe('[]')
