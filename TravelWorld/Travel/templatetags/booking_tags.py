# your_app/templatetags/booking_tags.py

from django import template
from ..models import HotelBooking, VehicleBooking, ActivityBooking, HouseboatBooking

register = template.Library()

@register.filter
def get_icon(item_type):
    """Returns a Font Awesome icon name based on the item type."""
    icon_map = {
        'Accommodation': 'hotel',
        'Transportation': 'car',
        'Activity': 'hiking',
        'Houseboat': 'ship',
    }
    return icon_map.get(item_type, 'question-circle') # a default icon

@register.filter
def get_item_name(booking):
    """Returns the main name for any booking object."""
    if isinstance(booking, HotelBooking):
        return booking.hotel.name
    if isinstance(booking, VehicleBooking):
        return booking.vehicle.name
    if isinstance(booking, ActivityBooking):
        return booking.activity.name
    if isinstance(booking, HouseboatBooking):
        return booking.houseboat.name
    return "Unknown Item"

@register.filter
def get_item_details(booking):
    """Returns the descriptive details for any booking object."""
    if isinstance(booking, HotelBooking):
        return f"{booking.room_type.name} - {booking.check_in_date.strftime('%d %b %Y')} to {booking.check_out_date.strftime('%d %b %Y')}"
    if isinstance(booking, VehicleBooking):
        return f"{booking.pickup_date.strftime('%d %b %Y')} @ {booking.pickup_time.strftime('%H:%M')} - {booking.vehicle_type}"
    if isinstance(booking, ActivityBooking):
        return f"{booking.booking_date.strftime('%d %b %Y')} @ {booking.booking_time.strftime('%H:%M')}"
    if isinstance(booking, HouseboatBooking):
        return f"{booking.meal_plan.name} - {booking.check_in_date.strftime('%d %b %Y')} to {booking.check_out_date.strftime('%d %b %Y')}"
    return ""


@register.filter
def get_model_name(obj):
    """Returns the name of the model's class."""
    return obj.__class__.__name__