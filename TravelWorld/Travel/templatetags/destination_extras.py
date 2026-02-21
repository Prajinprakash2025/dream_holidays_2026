# myapp/templatetags/destination_extras.py
from django import template

register = template.Library()

@register.filter
def get_name(destinations, id):
    try:
        return destinations.get(id=id).name
    except:
        return ""
