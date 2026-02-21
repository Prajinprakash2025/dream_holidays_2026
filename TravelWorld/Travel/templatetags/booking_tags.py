# your_app/templatetags/booking_tags.py

from django import template
from ..models import (
    HotelBooking, 
    VehicleBooking, 
    ActivityBooking, 
    HouseboatBooking
)

register = template.Library()


@register.filter
def get_icon(item_type):
    """Returns a Font Awesome icon class based on the item type."""
    icon_map = {
        'Accommodation': 'fas fa-hotel',
        'Transportation': 'fas fa-car',
        'Activity': 'fas fa-hiking',
        'Houseboat': 'fas fa-ship',
        'Inclusion': 'fas fa-star',
        'Hotel': 'fas fa-hotel',
        'Vehicle': 'fas fa-car',
    }
    return icon_map.get(item_type, 'fas fa-question-circle')


@register.filter
def get_icon_color(item_type):
    """Returns a Bootstrap color class based on the item type."""
    color_map = {
        'Accommodation': 'text-primary',
        'Hotel': 'text-primary',
        'Transportation': 'text-danger',
        'Vehicle': 'text-danger',
        'Activity': 'text-success',
        'Houseboat': 'text-info',
        'Inclusion': 'text-warning',
    }
    return color_map.get(item_type, 'text-secondary')


@register.filter
def get_item_name(booking):
    """Returns the main name for any booking object."""
    if booking is None:
        return "Unknown Item"
    
    if isinstance(booking, HotelBooking):
        return booking.hotel.name
    elif isinstance(booking, VehicleBooking):
        return booking.vehicle.name
    elif isinstance(booking, ActivityBooking):
        return booking.activity.name
    elif isinstance(booking, HouseboatBooking):
        return booking.houseboat.name
    elif hasattr(booking, 'special_inclusion'):
        # Handle standalone inclusions without importing the model
        return booking.special_inclusion.name
    
    return "Unknown Item"


@register.filter
def get_item_details(booking):
    """Returns the descriptive details for any booking object."""
    if booking is None:
        return ""
    
    try:
        if isinstance(booking, HotelBooking):
            room_type = booking.room_type.name if booking.room_type else "Standard Room"
            meal_plan = booking.meal_plan.name if booking.meal_plan else "No Meals"
            check_in = booking.check_in_date.strftime('%d %b %Y') if booking.check_in_date else "N/A"
            check_out = booking.check_out_date.strftime('%d %b %Y') if booking.check_out_date else "N/A"
            return f"{room_type} • {meal_plan} • {check_in} to {check_out}"
        
        elif isinstance(booking, VehicleBooking):
            pickup_date = booking.pickup_date.strftime('%d %b %Y') if booking.pickup_date else "N/A"
            pickup_time = booking.pickup_time.strftime('%H:%M') if hasattr(booking, 'pickup_time') and booking.pickup_time else "N/A"
            passengers = booking.num_passengers if booking.num_passengers else 0
            km = f" • {booking.total_km} km" if booking.total_km else ""
            return f"{pickup_date} @ {pickup_time} • {passengers} passengers{km}"
        
        elif isinstance(booking, ActivityBooking):
            booking_date = booking.booking_date.strftime('%d %b %Y') if booking.booking_date else "N/A"
            booking_time = booking.booking_time.strftime('%H:%M') if hasattr(booking, 'booking_time') and booking.booking_time else "N/A"
            participants = booking.num_participants if hasattr(booking, 'num_participants') and booking.num_participants else ""
            participant_text = f" • {participants} participants" if participants else ""
            return f"{booking_date} @ {booking_time}{participant_text}"
        
        elif isinstance(booking, HouseboatBooking):
            meal_plan = booking.meal_plan.name if booking.meal_plan else "No Meals"
            room_type = booking.room_type.name if booking.room_type else "Standard"
            check_in = booking.check_in_date.strftime('%d %b %Y') if booking.check_in_date else "N/A"
            check_out = booking.check_out_date.strftime('%d %b %Y') if booking.check_out_date else "N/A"
            return f"{room_type} • {meal_plan} • {check_in} to {check_out}"
        
        elif hasattr(booking, 'special_inclusion'):
            # Handle standalone inclusions
            adults = f"{booking.num_adults} Adults" if hasattr(booking, 'num_adults') and booking.num_adults else ""
            children = f"{booking.num_children} Children" if hasattr(booking, 'num_children') and booking.num_children else ""
            if adults and children:
                return f"{adults}, {children}"
            return adults or children or "Special Inclusion"
    
    except Exception as e:
        return ""
    
    return ""


@register.filter
def get_model_name(obj):
    """Returns the name of the model's class."""
    if obj is None:
        return "Unknown"
    return obj.__class__.__name__


@register.filter
def get_edit_url(booking):
    """Returns the appropriate edit URL name for a booking object."""
    url_map = {
        'HotelBooking': 'edit_hotel_booking',
        'VehicleBooking': 'edit_vehicle_booking',
        'ActivityBooking': 'edit_activity_booking',
        'HouseboatBooking': 'edit_houseboat_booking',
        'StandaloneInclusion': 'edit_standalone_inclusion',
    }
    model_name = get_model_name(booking)
    return url_map.get(model_name, '#')


@register.filter
def get_delete_url(booking):
    """Returns the appropriate delete URL name for a booking object."""
    url_map = {
        'HotelBooking': 'delete_hotel_booking',
        'VehicleBooking': 'delete_vehicle_booking',
        'ActivityBooking': 'delete_activity_booking',
        'HouseboatBooking': 'delete_houseboat_booking',
        'StandaloneInclusion': 'delete_standalone_inclusion',
    }
    model_name = get_model_name(booking)
    return url_map.get(model_name, '#')


@register.filter
def format_date_range(start_date, end_date):
    """Formats a date range nicely."""
    if not start_date or not end_date:
        return ""
    
    try:
        start = start_date.strftime('%d %b')
        end = end_date.strftime('%d %b %Y')
        return f"{start} - {end}"
    except:
        return ""


@register.filter
def get_booking_badge_class(booking):
    """Returns appropriate badge class for a booking type."""
    badge_map = {
        'HotelBooking': 'bg-primary',
        'VehicleBooking': 'bg-danger',
        'ActivityBooking': 'bg-success',
        'HouseboatBooking': 'bg-info',
        'StandaloneInclusion': 'bg-warning text-dark',
    }
    model_name = get_model_name(booking)
    return badge_map.get(model_name, 'bg-secondary')
