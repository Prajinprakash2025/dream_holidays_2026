# In yourapp/templatetags/pricing_filters.py
from django import template
import json

register = template.Library()

@register.filter(name='to_json')
def to_json(value):
    """Convert Python object to JSON string"""
    try:
        return json.dumps(value)
    except:
        return '[]'
