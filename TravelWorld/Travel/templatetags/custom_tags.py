# yourapp/templatetags/custom_tags.py
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Fetch a dictionary item by key in templates.
    Usage: {{ my_dict|get_item:key_name }}
    """
    if not dictionary:
        return None
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None


@register.filter
def get_stars(value):
    """
    Convert a numeric rating (1–5) into star symbols.
    Usage: {{ 3|get_stars }}
    Returns: ★★★☆☆
    """
    try:
        rating = int(value)
        rating = max(0, min(5, rating))  # Clamp between 0-5
    except (ValueError, TypeError):
        return ""
    return "★" * rating + "☆" * (5 - rating)


@register.filter
def replace_underscore(value):
    """
    Replace underscores with spaces and title case.
    Usage: {{ "standalone_inclusions"|replace_underscore }}
    Returns: "Standalone Inclusions"
    """
    if not isinstance(value, str):
        return value
    return value.replace('_', ' ').title()


@register.filter
def format_section_name(value):
    """
    Format section names for display.
    Usage: {{ "standalone_inclusions"|format_section_name }}
    Returns: "Standalone Activities"
    """
    section_names = {
        'hotels': 'Hotels',
        'houseboats': 'Houseboats',
        'activities': 'Activities',
        'vehicles': 'Vehicles',
        'standalone_inclusions': 'Standalone Activities',
    }
    return section_names.get(value, value.replace('_', ' ').title())
