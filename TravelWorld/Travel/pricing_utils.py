# pricing_utils.py
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from itertools import chain
from operator import attrgetter
from django.utils.timezone import now
from .models import (
    Itinerary, HotelBooking, VehicleBooking, ActivityBooking, HouseboatBooking,
    ItineraryPricingOption, Hotelprice, VehiclePricing, ActivityPrice, HouseboatPrice
)


def calculate_itinerary_pricing(itinerary, save=True):
    """
    Calculate and optionally save pricing for an itinerary based on current booking dates.
    This reuses the same logic from itinerary_pricing view.
    
    Args:
        itinerary: Itinerary instance
        save: Boolean - whether to save pricing options to database
    
    Returns:
        List of pricing option dictionaries
    """
    print(f"\n💰 Calculating prices for Itinerary #{itinerary.id}")
    print(f"   Using NEW booking dates for price lookup...")
    
    def calculate_booking_price(booking):
        """Calculate net price for a single booking based on its date"""
        net_price = Decimal('0.00')
        
        # --- Hotel Booking ---
        if isinstance(booking, HotelBooking):
            if hasattr(booking, 'net_price') and booking.net_price and booking.net_price > 0:
                net_price = booking.net_price
            else:
                nights = (booking.check_out_date - booking.check_in_date).days or 1
                rule = Hotelprice.objects.filter(
                    hotel=booking.hotel,
                    room_type=booking.room_type,
                    meal_plan=booking.meal_plan,
                    from_date__lte=booking.check_in_date,
                    to_date__gte=booking.check_in_date
                ).first()
                
                if rule:
                    per_night = (
                        Decimal(booking.num_double_beds or 0) * (rule.double_bed or 0) +
                        Decimal(booking.child_with_bed or 0) * (rule.child_with_bed or 0) +
                        Decimal(booking.child_without_bed or 0) * (rule.child_without_bed or 0) +
                        Decimal(booking.extra_beds or 0) * (rule.extra_bed or 0)
                    )
                    net_price = per_night * nights
                    print(f"   🏨 {booking.hotel.name}: ₹{per_night}/night × {nights} = ₹{net_price}")
                else:
                    print(f"   ⚠️ No price rule for {booking.hotel.name} on {booking.check_in_date}")
            
            booking.price_record = rule if 'rule' in locals() else None
            booking.sort_date = booking.check_in_date
            booking.item_type = 'Accommodation'
        
        # --- Vehicle Booking ---
        elif isinstance(booking, VehicleBooking):
            rule = VehiclePricing.objects.filter(
                vehicle=booking.vehicle,
                from_date__lte=booking.pickup_date,
                to_date__gte=booking.pickup_date,
                is_active=True
            ).first()
            
            expected_calculated_price = Decimal('0')
            if rule and hasattr(booking, 'total_km') and booking.total_km is not None:
                if booking.total_km <= 100:
                    expected_calculated_price = rule.total_fee_100km or Decimal('0')
                else:
                    extra_km = booking.total_km - 100
                    extra_cost = Decimal(str(extra_km)) * (rule.extra_fee_per_km or Decimal('0'))
                    expected_calculated_price = (rule.total_fee_100km or Decimal('0')) + extra_cost
            
            if hasattr(booking, 'custom_total_price') and booking.custom_total_price and booking.custom_total_price > 0:
                net_price = booking.custom_total_price
            elif hasattr(booking, 'net_price') and booking.net_price and booking.net_price > 0:
                net_price = booking.net_price
            else:
                net_price = expected_calculated_price
            
            print(f"   🚗 {booking.vehicle.name}: {booking.total_km}km = ₹{net_price}")
            booking.price_record = rule
            booking.sort_date = booking.pickup_date
            booking.item_type = 'Transportation'
        
        # --- Activity Booking ---
        elif isinstance(booking, ActivityBooking):
            rule = ActivityPrice.objects.filter(
                activity=booking.activity,
                from_date__lte=booking.booking_date,
                to_date__gte=booking.booking_date
            ).first() or ActivityPrice.objects.filter(activity=booking.activity).first()
            
            expected_calculated_price = Decimal('0')
            if rule:
                total_people = (booking.num_adults or 0) + (booking.num_children or 0)
                expected_calculated_price = Decimal(str(total_people)) * (rule.per_person or Decimal('0'))
            
            if hasattr(booking, 'custom_total_price') and booking.custom_total_price and booking.custom_total_price > 0:
                net_price = booking.custom_total_price
            elif hasattr(booking, 'net_price') and booking.net_price and booking.net_price > 0:
                net_price = booking.net_price
            else:
                net_price = expected_calculated_price
            
            print(f"   🎯 {booking.activity.name}: {total_people if 'total_people' in locals() else 0} people = ₹{net_price}")
            booking.price_record = rule
            booking.sort_date = booking.booking_date
            booking.item_type = 'Activity'
        
        # --- Houseboat Booking ---
        elif isinstance(booking, HouseboatBooking):
            if hasattr(booking, 'net_price') and booking.net_price and booking.net_price > 0:
                net_price = booking.net_price
            else:
                nights = (booking.check_out_date - booking.check_in_date).days or 1
                rule = HouseboatPrice.objects.filter(
                    houseboat=booking.houseboat,
                    meal_plan=booking.meal_plan,
                    room_type=booking.room_type,
                    from_date__lte=booking.check_in_date,
                    to_date__gte=booking.check_in_date
                ).first()
                
                if rule:
                    per_night = (
                        Decimal(booking.num_one_bed_rooms or 0) * (rule.one_bed or 0) +
                        Decimal(booking.num_two_bed_rooms or 0) * (rule.two_bed or 0) +
                        Decimal(booking.num_three_bed_rooms or 0) * (rule.three_bed or 0) +
                        Decimal(booking.num_four_bed_rooms or 0) * (rule.four_bed or 0) +
                        Decimal(booking.num_five_bed_rooms or 0) * (rule.five_bed or 0) +
                        Decimal(booking.num_six_bed_rooms or 0) * (rule.six_bed or 0) +
                        Decimal(booking.num_seven_bed_rooms or 0) * (rule.seven_bed or 0) +
                        Decimal(booking.num_eight_bed_rooms or 0) * (rule.eight_bed or 0) +
                        Decimal(booking.num_nine_bed_rooms or 0) * (rule.nine_bed or 0) +
                        Decimal(booking.num_ten_bed_rooms or 0) * (rule.ten_bed or 0) +
                        Decimal(booking.num_extra_beds or 0) * (rule.extra_bed or 0)
                    )
                    net_price = per_night * nights
            
            booking.price_record = rule if 'rule' in locals() else None
            booking.sort_date = booking.check_in_date
            booking.item_type = 'Houseboat'
            print(f"   🚤 {booking.houseboat.name}: ₹{net_price}")
        
        # Calculate individual markup
        individual_markup = Decimal('0.00')
        if hasattr(booking, 'markup_value') and booking.markup_value:
            try:
                markup_val = Decimal(str(booking.markup_value))
                if markup_val > 0:
                    if booking.markup_type != 'percentage':
                        individual_markup = markup_val
                    else:
                        individual_markup = net_price * (markup_val / 100)
            except (ValueError, TypeError, InvalidOperation):
                pass
        
        booking.calculated_price = {
            'net': net_price,
            'markup': individual_markup,
            'gross': net_price + individual_markup
        }
        return booking
    
    # Get all bookings
    combined_bookings = list(chain(
        HotelBooking.objects.filter(day_plan__itinerary=itinerary),
        VehicleBooking.objects.filter(itinerary=itinerary),
        ActivityBooking.objects.filter(day_plan__itinerary=itinerary),
        HouseboatBooking.objects.filter(day_plan__itinerary=itinerary)
    ))
    
    # Calculate prices for all bookings
    all_items = [calculate_booking_price(booking) for booking in combined_bookings]
    all_items = sorted(all_items, key=attrgetter('sort_date'))
    
    # Calculate non-accommodation totals
    non_accommodation_net = sum(
        item.calculated_price['net'] for item in all_items 
        if item.item_type != 'Accommodation'
    )
    
    # Group hotels by option
    grouped_hotels = defaultdict(list)
    for item in all_items:
        if item.item_type == 'Accommodation':
            hotel_option = getattr(item, 'option', 'Option 1')
            grouped_hotels[hotel_option].append(item)
    
    # If no hotels, create default option
    if not grouped_hotels:
        grouped_hotels['Standard Package'] = []
    
    pricing_options = []
    
    # Create pricing option for each hotel group
    for index, (option_name, hotels) in enumerate(grouped_hotels.items(), 1):
        option_hotels_net = sum(h.calculated_price['net'] for h in hotels)
        package_net = option_hotels_net + non_accommodation_net
        
        # Calculate taxes and final amount
        cgst_amount = package_net * (itinerary.cgst_percentage / Decimal('100'))
        sgst_amount = package_net * (itinerary.sgst_percentage / Decimal('100'))
        final_amount = package_net + cgst_amount + sgst_amount - itinerary.discount
        
        # Prepare hotel list
        hotels_list = [
            {'name': h.hotel.name, 'net_price': float(h.calculated_price['net'])}
            for h in hotels
        ]
        
        option_data = {
            'option_name': option_name,
            'option_number': index,
            'net_price': package_net,
            'gross_price': package_net,
            'cgst_amount': cgst_amount,
            'sgst_amount': sgst_amount,
            'discount_amount': itinerary.discount,
            'final_amount': final_amount,
            'hotels_included': hotels_list
        }
        
        pricing_options.append(option_data)
        
        print(f"\n   ✅ {option_name}:")
        print(f"      Net: ₹{package_net}")
        print(f"      CGST: ₹{cgst_amount}")
        print(f"      SGST: ₹{sgst_amount}")
        print(f"      Final: ₹{final_amount}")
    
    # Save to database if requested
    if save:
        # Clear existing options
        ItineraryPricingOption.objects.filter(itinerary=itinerary).delete()
        
        # Create new options
        for option_data in pricing_options:
            ItineraryPricingOption.objects.create(
                itinerary=itinerary,
                **option_data
            )
        
        # Mark itinerary as finalized
        itinerary.is_finalized = True
        itinerary.finalized_at = now()
        itinerary.save()
        
        print(f"\n   💾 Saved {len(pricing_options)} pricing option(s) to database")
    
    return pricing_options
