from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone


def get_default_team_member():
    return TeamMember.objects.first().id



class Supplier(models.Model):
    """
    Generic Supplier model that can be used for Hotels, Activities, Vehicles, Houseboats, and Special Inclusions.
    """
    SUPPLIER_TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('activity', 'Activity'),
        ('vehicle', 'Vehicle'),
        ('houseboat', 'Houseboat'),
        ('standalone_inclusion', 'Special Inclusion'),  # NEW
        ('other', 'Other'),
    ]

    # Basic Info
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255, db_index=True)
    supplier_type = models.CharField(
        max_length=30,  # Increased from 20 to accommodate 'standalone_inclusion'
        choices=SUPPLIER_TYPE_CHOICES,
        default='other',
        help_text="Type of supplier service"
    )

    # Contact Person
    supplier_first_name = models.CharField(max_length=100)
    supplier_last_name = models.CharField(max_length=100)

    # Contact Details
    email = models.EmailField(db_index=True)
    mobile_no = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=15, blank=True, null=True)

    # Address
    address = models.TextField()
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    # Business Info
    gst_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Status & Timestamps
    is_active = models.BooleanField(default=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Notes
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'supplier_type']),
            models.Index(fields=['company_name']),
        ]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return f"{self.company_name} - {self.supplier_first_name} {self.supplier_last_name} ({self.get_supplier_type_display()})"

    @property
    def full_name(self):
        """Returns the full name of the contact person"""
        return f"{self.supplier_first_name} {self.supplier_last_name}"

    @property
    def contact_info(self):
        """Returns formatted contact information"""
        return f"{self.email} | {self.mobile_no}"

    def get_type_icon(self):
        """Returns emoji/icon for supplier type"""
        icons = {
            'hotel': '🏨',
            'activity': '🎯',
            'vehicle': '🚗',
            'houseboat': '🚤',
            'standalone_inclusion': '⭐',
            'other': '📦',
        }
        return icons.get(self.supplier_type, '📦')

    def get_active_status_display(self):
        """Returns human-readable active status"""
        return "Active" if self.is_active else "Inactive"

    def get_verified_status_display(self):
        """Returns human-readable verified status"""
        return "Verified" if self.is_verified else "Not Verified"



class Destinations(models.Model):
    name = models.CharField(max_length=100, unique=True)

    default_image = models.ImageField(
        upload_to='destination_images/',
        blank=True,
        null=True,
        help_text="Default image for this destination"
    )

    default_description = models.TextField(
        blank=True,
        null=True,
        help_text="Default itinerary description for this destination"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now, editable=False)


    def save(self, *args, **kwargs):
        # Optional: Force lowercase or title case to prevent "Kochi" vs "kochi" duplicates
        self.name = self.name.lower()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name



class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name


from django.contrib.auth.hashers import make_password, check_password

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('cre','Cre')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255,null=True)

    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(default=now, editable=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
    def has_permission(self, permission_name):
        """Check if user has a specific permission"""
        if self.role == 'admin':
            return True  # Admins have all permissions
        return self.permissions.get(permission_name, False)

    def grant_permission(self, permission_name):
        """Grant a permission"""
        self.permissions[permission_name] = True
        self.save()

    def revoke_permission(self, permission_name):
        """Revoke a permission"""
        self.permissions[permission_name] = False
        self.save()

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def phone(self):
        return self.phone_number

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_role_display_badge(self):
        colors = {
            'admin': 'danger',
            'manager': 'warning',
            'staff': 'info',
            'cre': 'primary'
        }
        return colors.get(self.role, 'secondary')

##############for connecting with php site#########################


class Lead(models.Model):
    # Basic info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Team Member assignment
    assigned_to = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
        help_text="The TeamMember responsible for this lead"
    )

    # Tracking fields
    from_url = models.URLField(blank=True, null=True, help_text="Landing page / form URL")
    from_domain = models.CharField(max_length=200, blank=True)

    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=200, blank=True)
    utm_term = models.CharField(max_length=200, blank=True)

    gclid = models.CharField(max_length=255, blank=True)  # Google Ads click id
    is_ads = models.BooleanField(default=False)

    source = models.CharField(max_length=100, blank=True)  # e.g. "dream-holidays-php"

    def save(self, *args, **kwargs):
        # Extract domain from URL
        if self.from_url:
            try:
                self.from_domain = urlparse(self.from_url).netloc
            except Exception:
                pass

        # Classify as Google Ads lead
        self.is_ads = bool(
            self.gclid
            or (self.utm_source.lower() == "google" and
                self.utm_medium.lower() in {"cpc", "ppc", "paid", "paid_search"})
        )

        super().save(*args, **kwargs)

    @property
    def channel(self):
        """Returns readable marketing channel name."""
        if self.is_ads:
            return "Google Ads"
        if self.utm_source:
            if self.utm_medium:
                return f"{self.utm_source.title()} / {self.utm_medium}"
            return self.utm_source.title()
        if self.from_domain:
            return f"Referral ({self.from_domain})"
        return "Direct"

    def __str__(self):
        return self.name




class MealPlan(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=True)  # Active or Not
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-filled timestamp
    created_by = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, default=get_default_team_member
    )


    def __str__(self):
        return self.name

class  Hotel(models.Model):
    CATEGORY_CHOICES = [
        ('budget', 'Budget'),
        ('1star', '1 Star'),
        ('2star', '2 Star'),
        ('3star', '3 Star'),
        ('4star', '4 Star'),
        ('5star', '5 Star'),
        ('luxury', 'Luxury'),
        ('resort', 'Resort'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    details = models.TextField()
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hotels',
        limit_choices_to={'supplier_type': 'hotel', 'is_active': True},
        help_text="Supplier who owns/manages this hotel")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # Extra phone
    status = models.BooleanField(default=True)  # Active or not
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    hotel_link = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def supplier_name(self):
        """Get supplier company name"""
        return self.supplier.company_name if self.supplier else 'No Supplier'

    @property
    def supplier_contact(self):
        """Get supplier contact details"""
        if self.supplier:
            return f"{self.supplier.full_name} - {self.supplier.mobile_no}"
        return "N/A"


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f"Image for {self.hotel.name}"

from django.db.models import UniqueConstraint

class Hotelprice(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='prices')
    from_date = models.DateField()
    to_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)

    double_bed = models.DecimalField(max_digits=10, decimal_places=2)
    child_without_bed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    child_with_bed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    extra_bed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['hotel', 'room_type', 'meal_plan', 'from_date', 'to_date'],
                name='unique_hotel_room_meal_date_range'
            )
        ]

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.name} ({self.from_date} to {self.to_date})"

from django.db import models
from decimal import Decimal
import json

class HotelBookingInclusion(models.Model):
    """
    Model to track multiple special inclusions per hotel booking.
    Works for both Package Template bookings and Itinerary bookings
    through the HotelBooking relationship.
    """
    hotel_booking = models.ForeignKey(
        'HotelBooking',
        on_delete=models.CASCADE,
        related_name='inclusion_items'
    )
    special_inclusion = models.ForeignKey(
        'SpecialInclusion',
        on_delete=models.CASCADE
    )
    num_adults = models.PositiveIntegerField(
        default=0,
        verbose_name="Adults with this Inclusion"
    )
    num_children = models.PositiveIntegerField(
        default=0,
        verbose_name="Children with this Inclusion"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total Price for this Inclusion Item"
    )

    class Meta:
        verbose_name = "Hotel Booking Inclusion"
        verbose_name_plural = "Hotel Booking Inclusions"
        ordering = ['id']

    def __str__(self):
        # Show badge based on parent booking type
        type_badge = "[PKG]" if self.is_package_booking else "[ITN]"
        return f"{type_badge} {self.special_inclusion.name} - {self.num_adults}A + {self.num_children}C (₹{self.price})"

    # ✅ Properties to determine booking type via HotelBooking
    @property
    def is_package_booking(self):
        """Check if this belongs to a package template booking"""
        return self.hotel_booking.package_template_id is not None

    @property
    def is_itinerary_booking(self):
        """Check if this belongs to an itinerary booking"""
        return self.hotel_booking.itinerary_id is not None

    @property
    def booking_type(self):
        """Get the booking type as a string"""
        if self.is_package_booking:
            return 'package'
        elif self.is_itinerary_booking:
            return 'itinerary'
        return 'unknown'

    @property
    def parent_name(self):
        """Get the name of the parent (package or itinerary)"""
        if self.is_package_booking:
            return self.hotel_booking.package_template.name
        elif self.is_itinerary_booking:
            return self.hotel_booking.itinerary.name
        return "Unknown"

    @property
    def parent_object(self):
        """Get the actual parent object (PackageTemplate or Itinerary)"""
        if self.is_package_booking:
            return self.hotel_booking.package_template
        elif self.is_itinerary_booking:
            return self.hotel_booking.itinerary
        return None

    def calculate_price(self):
        """Calculate price based on adults, children, and inclusion pricing"""
        if not self.special_inclusion:
            return Decimal('0.00')

        inclusion = self.special_inclusion

        if inclusion.pricing_type == 'free':
            return Decimal('0.00')

        if inclusion.pricing_type == 'per_booking':
            return inclusion.adult_price

        if inclusion.pricing_type == 'per_room':
            # Use num_rooms from the hotel booking
            num_rooms = self.hotel_booking.num_rooms or 1
            return inclusion.adult_price * num_rooms

        if inclusion.pricing_type == 'per_person':
            adult_price = inclusion.adult_price * self.num_adults
            child_price = inclusion.get_child_price() * self.num_children
            return adult_price + child_price

        return Decimal('0.00')

    def save(self, *args, **kwargs):
        """Auto-calculate price before saving"""
        self.price = self.calculate_price()
        super().save(*args, **kwargs)



from django.db import models
from django.utils.timezone import now

class Houseboat(models.Model):
    HOUSEBOAT_TYPE_CHOICES = [
        ('traditional', 'Traditional Houseboat'),
        ('luxury', 'Luxury Houseboat'),
        ('budget', 'Budget Houseboat'),
        ('premium', 'Premium Houseboat'),
    ]

    name = models.CharField(max_length=255)
    destination = models.ForeignKey(
        'Destinations',
        on_delete=models.CASCADE,
        related_name='houseboats'
    )
    details = models.TextField()
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'TeamMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 NEW: Supplier Relationship
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='houseboats',
        limit_choices_to={'supplier_type': 'houseboat', 'is_active': True},
        help_text="Supplier who owns/manages this houseboat"
    )

    # Additional Details
    houseboat_type = models.CharField(
        max_length=20,
        choices=HOUSEBOAT_TYPE_CHOICES,
        default='traditional',
        help_text="Type of houseboat"
    )

    length_meters = models.FloatField(
        default=15.0,
        help_text="Length of houseboat in meters"
    )

    total_capacity = models.PositiveIntegerField(
        default=20,
        help_text="Total number of people capacity"
    )

    num_cabins = models.PositiveIntegerField(
        default=5,
        help_text="Number of cabins/rooms"
    )

    num_bathrooms = models.PositiveIntegerField(
        default=5,
        help_text="Number of bathrooms"
    )

    image = models.ImageField(
        upload_to='houseboats/',
        blank=True,
        null=True,
        help_text="Main image of houseboat"
    )

    phone_alternate = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Alternate phone number"
    )

    website = models.URLField(
        blank=True,
        null=True,
        help_text="Houseboat website"
    )

    amenities = models.TextField(
        blank=True,
        null=True,
        help_text="List amenities (e.g., A/C, Hot water, WiFi, Kitchen, etc.)"
    )

    special_features = models.TextField(
        blank=True,
        null=True,
        help_text="Special features (e.g., Rooftop deck, Spa, Restaurant, etc.)"
    )

    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text="Houseboat registration/license number"
    )

    is_premium = models.BooleanField(
        default=False,
        help_text="Mark as premium listing"
    )

    maximum_stay_days = models.PositiveIntegerField(
        default=30,
        help_text="Maximum number of days for booking"
    )

    class Meta:
        verbose_name = "Houseboat"
        verbose_name_plural = "Houseboats"
        ordering = ['-created_at']
        db_table = "houseboat"
        indexes = [
            models.Index(fields=['status', 'destination']),
            models.Index(fields=['supplier']),
            models.Index(fields=['houseboat_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_houseboat_type_display()})"

    @property
    def supplier_name(self):
        """Get supplier company name"""
        return self.supplier.company_name if self.supplier else 'No Supplier'

    @property
    def supplier_contact(self):
        """Get supplier contact details"""
        if self.supplier:
            return f"{self.supplier.full_name} - {self.supplier.mobile_no}"
        return "N/A"

    @property
    def availability_status(self):
        """Check if houseboat is available"""
        return "Available" if self.status else "Unavailable"

    @property
    def rating_badge(self):
        """Get premium status badge"""
        return "⭐ Premium" if self.is_premium else "Standard"



class HouseboatImage(models.Model):
    houseboat = models.ForeignKey(
        Houseboat,
        on_delete=models.CASCADE,
        related_name="images"   # lets you do houseboat.images.all()
    )
    image = models.ImageField(upload_to="houseboats/")

    def __str__(self):
        return f"Image for {self.houseboat.name}"




class HouseboatPrice(models.Model):
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    one_bed = models.DecimalField(max_digits=10, decimal_places=1)
    two_bed = models.DecimalField(max_digits=10, decimal_places=1)
    three_bed = models.DecimalField(max_digits=10, decimal_places=1)
    four_bed = models.DecimalField(max_digits=10, decimal_places=1)
    five_bed = models.DecimalField(max_digits=10, decimal_places=1)
    six_bed = models.DecimalField(max_digits=10, decimal_places=1)
    seven_bed = models.DecimalField(max_digits=10, decimal_places=1)
    eight_bed = models.DecimalField(max_digits=10, decimal_places=1)
    nine_bed = models.DecimalField(max_digits=10, decimal_places=1)
    ten_bed = models.DecimalField(max_digits=10, decimal_places=1)
    extra_bed = models.DecimalField(max_digits=10, decimal_places=1)


    def __str__(self):
        return f"{self.houseboat.name} ({self.from_date} - {self.to_date})"










class Activity(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
        ('expert', 'Expert'),
    ]

    ACTIVITY_TYPE_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('religious', 'Religious'),
        ('water_sports', 'Water Sports'),
        ('trekking', 'Trekking'),
        ('tour', 'Guided Tour'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('dining', 'Dining'),
        ('wellness', 'Wellness'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    destination = models.ForeignKey(
        'Destinations',
        on_delete=models.CASCADE,
        related_name='activities'
    )
    details = models.TextField()
    photo = models.ImageField(upload_to='activities/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'TeamMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 NEW: Supplier Relationship
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        limit_choices_to={'supplier_type': 'activity', 'is_active': True},
        help_text="Supplier who provides this activity"
    )

    # Additional Details
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES,
        default='tour',
        help_text="Type of activity"
    )

    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='moderate',
        help_text="Difficulty level of activity"
    )

    duration_hours = models.FloatField(
        default=2.0,
        help_text="Duration in hours"
    )

    max_participants = models.PositiveIntegerField(
        default=20,
        help_text="Maximum number of participants"
    )

    min_participants = models.PositiveIntegerField(
        default=1,
        help_text="Minimum number of participants"
    )

    age_restriction = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Age restrictions, if any (e.g., 'Minimum 18 years')"
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Contact person for activity"
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )

    meeting_point = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Meeting point/location"
    )

    inclusions = models.TextField(
        blank=True,
        null=True,
        help_text="What's included (e.g., guide, equipment, meals)"
    )

    exclusions = models.TextField(
        blank=True,
        null=True,
        help_text="What's not included"
    )

    website = models.URLField(
        blank=True,
        null=True,
        help_text="Activity website"
    )

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'destination']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['supplier']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_activity_type_display()})"

    @property
    def supplier_name(self):
        """Get supplier company name"""
        return self.supplier.company_name if self.supplier else 'No Supplier'

    @property
    def supplier_contact(self):
        """Get supplier contact details"""
        if self.supplier:
            return f"{self.supplier.full_name} - {self.supplier.mobile_no}"
        return "N/A"

    @property
    def is_available(self):
        """Check if activity is available"""
        return self.is_active

    @property
    def availability_status(self):
        """Get human-readable availability status"""
        return "Available" if self.is_active else "Unavailable"


from django.core.exceptions import ValidationError
from django.db import models

class ActivityPrice(models.Model):
    # Added 'related_name' so you can use activity.prices.all() easily
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='prices')
    from_date = models.DateField()
    to_date = models.DateField()
    per_person = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.activity.name} ({self.from_date} - {self.to_date})"

    # This ensures data integrity even if saved outside a form
    def clean(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From Date cannot be after To Date")





# ==========================================
# 1. MASTER INCLUSION TYPES (NEW)
# ==========================================
class InclusionType(models.Model):
    """
    Master list of reusable inclusion types.
    Can be used across hotels and houseboats.
    """
    CATEGORY_CHOICES = [
        ('amenity', 'Amenity/Service'),
        ('transport', 'Transportation'),
        ('food', 'Food & Beverage'),
        ('upgrade', 'Room Upgrade'),
        ('experience', 'Experience/Tour'),
        ('facility', 'Facility Access'),
        ('flexibility', 'Booking Flexibility'),
        ('activity', 'Activity'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255, help_text="e.g., 'Airport Pickup', 'Spa Access'")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, help_text="What this inclusion provides")
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Inclusion Type"
        verbose_name_plural = "Inclusion Types"

    def __str__(self):
        return f"{self.name}"


class SpecialInclusion(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('houseboat', 'Houseboat'),
        ('general', 'General/Standalone'),
    ]

    PRICING_TYPE_CHOICES = [
        ('free', 'Complimentary (Free)'),
        ('per_person', 'Per Person'),
        ('per_room', 'Per Room'),
        ('per_booking', 'Per Booking'),
    ]

    CHILD_PRICING_CHOICES = [
        ('same', 'Same as Adult'),
        ('percentage', 'Percentage of Adult Price'),
        ('fixed', 'Fixed Price'),
        ('free', 'Free for Children'),
    ]

    # Basic Info
    name = models.CharField(max_length=255)
    inclusion_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True, related_name='special_inclusions')
    houseboat = models.ForeignKey('Houseboat', on_delete=models.CASCADE, null=True, blank=True, related_name='special_inclusions')
    destination = models.ForeignKey('Destinations', on_delete=models.SET_NULL, null=True, blank=True)

    # Adult Pricing
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE_CHOICES, default='free')
    adult_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Adult Price",
        help_text="Price for adults"
    )

    # ✅ NEW: Child Pricing
    child_pricing_type = models.CharField(
        max_length=20,
        choices=CHILD_PRICING_CHOICES,
        default='same',
        verbose_name="Child Pricing Type"
    )
    child_price_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Child Price/Percentage",
        help_text="Fixed price OR percentage (e.g., 50 for 50%)"
    )

    # Age Restrictions (Optional)
    min_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Minimum age for this inclusion (leave empty if no restriction)"
    )
    max_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum age for child pricing (e.g., 12)"
    )

    # Other Fields
    details = models.TextField()
    photo = models.ImageField(upload_to='inclusions/', blank=True, null=True)
    status = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Special Inclusion"
        verbose_name_plural = "Special Inclusions"

    def get_child_price(self):
        """Calculate and return child price based on pricing type"""
        if self.child_pricing_type == 'same':
            return self.adult_price
        elif self.child_pricing_type == 'percentage':
            return (self.adult_price * self.child_price_value) / 100
        elif self.child_pricing_type == 'fixed':
            return self.child_price_value
        elif self.child_pricing_type == 'free':
            return 0
        return self.adult_price

    def get_price_display(self):
        """Human-readable price display"""
        if self.pricing_type == 'free':
            return "FREE"

        adult_display = f"Adult: ₹{self.adult_price}"

        if self.child_pricing_type == 'same':
            child_display = "Child: Same as Adult"
        elif self.child_pricing_type == 'percentage':
            child_display = f"Child: {self.child_price_value}% of Adult (₹{self.get_child_price():.2f})"
        elif self.child_pricing_type == 'fixed':
            child_display = f"Child: ₹{self.child_price_value}"
        elif self.child_pricing_type == 'free':
            child_display = "Child: FREE"
        else:
            child_display = "Child: Same as Adult"

        return f"{adult_display} | {child_display}"

    def __str__(self):
        return f"{self.name} - {self.get_price_display()}"



# ==========================================
# 3. KEEP InclusionPrice (for seasonal pricing)
# ==========================================
class InclusionPrice(models.Model):
    """
    Seasonal pricing for inclusions.
    Overrides default_price in SpecialInclusion.
    """
    inclusion = models.ForeignKey(SpecialInclusion, on_delete=models.CASCADE, related_name='seasonal_prices')
    from_date = models.DateField()
    to_date = models.DateField()
    per_person_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['from_date']
        verbose_name = "Inclusion Seasonal Price"
        verbose_name_plural = "Inclusion Seasonal Prices"

    def __str__(self):
        return f"{self.inclusion.name} ({self.from_date} - {self.to_date}): ₹{self.per_person_price}"





from django.utils.timezone import now

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('bus', 'Bus'),
        ('truck', 'Truck'),
        ('tempo', 'Tempo'),
        ('auto', 'Auto'),
    ]

    name = models.CharField(max_length=255)
    destination = models.ForeignKey('Destinations', on_delete=models.CASCADE)
    details = models.TextField()
    photo = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True)

    # 🔥 NEW: Vehicle Type & Supplier Relationship
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        default='car',
        help_text="Type of vehicle"
    )

    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles',
        limit_choices_to={'supplier_type': 'vehicle', 'is_active': True},
        help_text="Supplier who owns/manages this vehicle"
    )

    # Additional Details
    capacity = models.PositiveIntegerField(
        default=4,
        help_text="Number of seats/capacity"
    )

    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text="Vehicle registration number"
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Driver or contact person name"
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Driver or contact phone number"
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'destination']),
            models.Index(fields=['supplier']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"

    @property
    def supplier_name(self):
        """Get supplier company name"""
        return self.supplier.company_name if self.supplier else 'No Supplier'

    @property
    def supplier_contact(self):
        """Get supplier contact details"""
        if self.supplier:
            return f"{self.supplier.full_name} - {self.supplier.mobile_no}"
        return "N/A"

    @property
    def availability_status(self):
        """Check if vehicle is available"""
        return "Active" if self.status else "Inactive"



class VehiclePricing(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    TYPE_CHOICES = [('PVT', 'Private')]
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='PVT')
    total_fee_100km = models.DecimalField(max_digits=10, decimal_places=2)
    extra_fee_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle.name} ({self.from_date} - {self.to_date})"





from django.db import models

class ItineraryImageGallery(models.Model):
    """Reusable gallery for day itinerary images"""
    name = models.CharField(
        max_length=255,
        help_text="Image name (e.g., 'Sunset Beach', 'Mountain View')"
    )
    image = models.ImageField(
        upload_to='itinerary_gallery/',
        help_text="Upload reusable itinerary image"
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Itinerary Gallery Image"
        verbose_name_plural = "Itinerary Gallery Images"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class DayItinerary(models.Model):
    IMAGE_SOURCE_CHOICES = [
        ('gallery', 'From Gallery'),
        ('upload', 'Upload New'),
    ]

    destination = models.CharField(
        max_length=255,
        help_text="Enter destination name (e.g., 'Munnar', 'Cochin')"
    )
    name = models.CharField(
        max_length=255,
        help_text="e.g., 'Cochin to Munnar (135 Km, 3.00 Hrs)'"
    )
    details = models.TextField(help_text="Full day itinerary description")

    # ✅ Image source choice
    image_source = models.CharField(
        max_length=10,
        choices=IMAGE_SOURCE_CHOICES,
        default='upload',
        help_text="Choose image from gallery or upload new"
    )

    # ✅ Gallery image (foreign key)
    gallery_image = models.ForeignKey(
        ItineraryImageGallery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='day_itineraries',
        help_text="Select from existing gallery images"
    )

    # ✅ Direct upload image (renamed from 'image')
    uploaded_image = models.ImageField(
        upload_to='day_itinerary_images/',
        blank=True,
        null=True,
        help_text="Upload new image directly"
    )

    is_pinned = models.BooleanField(
        default=False,
        help_text="Pin this itinerary to show first"
    )

    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Day Itinerary"
        verbose_name_plural = "Day Itineraries"
        ordering = ['-is_pinned', '-created_at']

    def get_image(self):
        """Returns the appropriate image based on source"""
        if self.image_source == 'gallery' and self.gallery_image:
            return self.gallery_image.image.url
        elif self.image_source == 'upload' and self.uploaded_image:
            return self.uploaded_image.url
        return None

    def __str__(self):
        pin = "📌 " if self.is_pinned else ""
        return f"{pin}{self.name} - {self.destination}"






class LeadSource(models.Model):
    source_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Using Django's built-in User; if you prefer your custom TeamMember, replace with that model.
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.source_name


class PackageTheme(models.Model):
    package_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='package_themes/', blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.package_name


class Currency(models.Model):
    currency_name = models.CharField(max_length=100)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.currency_name

class OrganisationalSetting(models.Model):
    organization_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    gstn = models.CharField(max_length=50, verbose_name="GSTN")
    state = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10)

    def __str__(self):
        return self.organization_name



class InvoiceLogo(models.Model):
    image = models.ImageField(upload_to='invoice_themes/', blank=True, null=True)

    def __str__(self):
        return "Invoice Logo"

class InvoiceTerms(models.Model):
    content = RichTextField()

    def __str__(self):
        return "Invoice Terms & Conditions"

class PackageTerms(models.Model):
    content = RichTextField(blank=True, null=True)

    def __str__(self):
        return "Package Terms & Conditions"

class BankInformation(models.Model):
    content = RichTextField()

    def __str__(self):
        return "Bank Information"


from ckeditor.fields import RichTextField
from django.db import models

class PackageTermss(models.Model):
    # Inclusions
    special_inclusion = RichTextField(blank=True, null=True, verbose_name="Special Inclusion")
    package_inclusion = RichTextField(blank=True, null=True, verbose_name="Package Inclusion")

    # Exclusions
    package_exclusion = RichTextField(blank=True, null=True, verbose_name="Package Exclusion")

    # Policies
    terms_and_conditions = RichTextField(blank=True, null=True, verbose_name="Terms and Conditions")
    payment_policy = RichTextField(blank=True, null=True, verbose_name="Payment Policy")
    cancellation_policy = RichTextField(blank=True, null=True, verbose_name="Cancellation Policy")
    refund_policy = RichTextField(blank=True, null=True, verbose_name="Refund After Cancellation")

    # Documents
    list_of_documents = RichTextField(blank=True, null=True, verbose_name="List of Documents Required")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Package Terms"
        verbose_name_plural = "Package Terms"
        ordering = ['-created_at']

    def __str__(self):
        return f"Package Terms (Active)" if self.is_active else f"Package Terms {self.id}"


class ItineraryPackageTerms(models.Model):
    """Itinerary-specific package terms that override default PackageTerms"""
    itinerary = models.OneToOneField(
        'Itinerary',
        on_delete=models.CASCADE,
        related_name='custom_package_terms',
        verbose_name="Itinerary"
    )

    # Inclusions
    special_inclusion = RichTextField(blank=True, null=True, verbose_name="Special Inclusion")
    package_inclusion = RichTextField(blank=True, null=True, verbose_name="Package Inclusion")

    # Exclusions
    package_exclusion = RichTextField(blank=True, null=True, verbose_name="Package Exclusion")

    # Policies
    terms_and_conditions = RichTextField(blank=True, null=True, verbose_name="Terms and Conditions")
    payment_policy = RichTextField(blank=True, null=True, verbose_name="Payment Policy")
    cancellation_policy = RichTextField(blank=True, null=True, verbose_name="Cancellation Policy")
    refund_policy = RichTextField(blank=True, null=True, verbose_name="Refund After Cancellation")

    # Documents
    list_of_documents = RichTextField(blank=True, null=True, verbose_name="List of Documents Required")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Itinerary Package Terms"
        verbose_name_plural = "Itinerary Package Terms"
        ordering = ['-created_at']

    def __str__(self):
        return f"Custom Terms for {self.itinerary.query.client_name}"

    @classmethod
    def get_or_create_from_default(cls, itinerary):
        """Create itinerary-specific terms from default PackageTerms"""
        custom_terms, created = cls.objects.get_or_create(itinerary=itinerary)

        if created:
            # Copy from default PackageTerms
            default_terms = PackageTermss.objects.first()
            if default_terms:
                custom_terms.special_inclusion = default_terms.special_inclusion
                custom_terms.package_inclusion = default_terms.package_inclusion
                custom_terms.package_exclusion = default_terms.package_exclusion
                custom_terms.terms_and_conditions = default_terms.terms_and_conditions
                custom_terms.payment_policy = default_terms.payment_policy
                custom_terms.cancellation_policy = default_terms.cancellation_policy
                custom_terms.refund_policy = default_terms.refund_policy
                custom_terms.list_of_documents = default_terms.list_of_documents
                custom_terms.save()

        return custom_terms, created



class BranchSettings(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    branch_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.branch_name


class Role(models.Model):
    PARENT_CHOICES = (
        ('Parent', 'Parent'),
        ('No Parent', 'No Parent'),
    )

    brand_name = models.ForeignKey(BranchSettings, on_delete=models.CASCADE)
    parent_selection = models.CharField(max_length=20, choices=PARENT_CHOICES)
    role_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name


class Query(models.Model):
    TYPE_CHOICES = [
        ('client', 'Client'),
        ('agent', 'Agent'),
        ('corporate', 'Corporate'),
    ]

    GENDER_CHOICES = [
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),
        ('dr', 'Dr'),
        ('prof', 'Prof'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('active', 'Active'),
        ('no_connect', 'No Connect'),
        ('follow_up', 'Follow Up'),
        ('proposal_sent', 'Proposal Sent'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('invalid', 'Invalid'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    SECTOR_CHOICES = [
        ('kerala', 'Kerala'),
        ('tamilnadu', 'Tamil Nadu'),
    ]

    PRIORITY_CHOICES = [
        ('general', 'General'),
        ('hot', 'Hot'),
    ]

    SERVICE_CHOICES = [
        ('activities', 'Activities Only'),
        ('flights', 'Flights Only'),
        ('full_package', 'Full Package'),
        ('hotel_flight', 'Hotel + Flight'),
        ('hotel_transport', 'Hotel + Transport'),
        ('hotel_only', 'Hotel Only'),
        ('transport_only', 'Transport Only'),
        ('visa_only', 'Visa Only'),
    ]

    # Custom Query ID field
    query_id = models.CharField(max_length=20, unique=True, editable=False, blank=True, db_index=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    client_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    total_days = models.PositiveIntegerField()
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    adult = models.PositiveIntegerField(null=True, blank=True)
    childrens = models.PositiveIntegerField(null=True, blank=True)
    infant = models.PositiveIntegerField(null=True, blank=True)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assign = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
    services = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now, editable=False)
    created_by = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_queries',
        help_text="Team member who created this query"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.query_id:
            # Get the last query to determine the next number
            last_query = Query.objects.all().order_by('id').last()
            if last_query and last_query.query_id:
                # Extract number from last query_id (e.g., 'dh01' -> 1)
                try:
                    last_num = int(last_query.query_id[2:])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            self.query_id = f'dh{new_num:02d}'  # Format: dh01, dh02, dh03...
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.query_id} - {self.client_name} - {self.phone_number}"






from decimal import Decimal
from django.db import models
from django.utils.timezone import now

class Itinerary(models.Model):
    # ============================================
    # BASIC INFO
    # ============================================
    name = models.CharField(max_length=255, verbose_name="Itinerary Name")
    query = models.ForeignKey('Query', on_delete=models.CASCADE, related_name='itineraries')
    destinations = models.ManyToManyField('Destinations', blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(
        'TeamMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_itineraries',
        verbose_name="Created By"
    )

    # ============================================
    # TRAVEL DATES (Independent from Query)
    # ============================================
    travel_from = models.DateField(null=True, blank=True, verbose_name="Travel Start Date")
    travel_to = models.DateField(null=True, blank=True, verbose_name="Travel End Date")
    total_days = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Days")

    # ============================================
    # PASSENGER COUNTS (Independent from Query)
    # ============================================
    adults = models.PositiveIntegerField(null=True, blank=True, verbose_name="Adults")
    childrens = models.PositiveIntegerField(null=True, blank=True, verbose_name="Children")
    infants = models.PositiveIntegerField(null=True, blank=True, verbose_name="Infants")

    # ============================================
    # PRICING FIELDS
    # ============================================
    total_net_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_gross_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    MARKUP_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount (₹)'),
        ('percentage', 'Percentage (%)')
    ]
    markup_type = models.CharField(
        max_length=10,
        choices=MARKUP_TYPE_CHOICES,
        default='fixed'
    )
    markup_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Fixed amount or percentage rate"
    )
    total_individual_markup = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )
    global_markup = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    # ============================================
    # STATUS & FINALIZATION
    # ============================================
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('quoted', 'Quoted'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Status"
    )

    is_finalized = models.BooleanField(default=False, verbose_name="Is Finalized")
    finalized_at = models.DateTimeField(blank=True, null=True, verbose_name="Finalized At")
    selected_option = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Selected Option"
    )

    # ============================================
    # VERSIONING & HISTORY (NO DUPLICATES!)
    # ============================================
    parent_itinerary = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versions',
        verbose_name="Previous Version",
        help_text="Link to the original itinerary when editing creates a new version"
    )

    version_number = models.IntegerField(
        default=1,
        verbose_name="Version Number",
        help_text="Version number of this itinerary (1, 2, 3...)"
    )

    archived_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Archived At",
        help_text="When this itinerary was moved to history/archived"
    )

    archived_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Archive Reason",
        help_text="Why was this itinerary archived"
    )

    # ============================================
    # META OPTIONS
    # ============================================
    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['parent_itinerary', 'status']),
            models.Index(fields=['query', 'status']),
            models.Index(fields=['version_number']),  # ✅ Added
        ]

    # ============================================
    # METHODS
    # ============================================
    def start_date(self):
        """Return itinerary travel_from or fallback to Query's from_date"""
        return self.travel_from or self.query.from_date

    def end_date(self):
        """Return itinerary travel_to or fallback to Query's to_date"""
        return self.travel_to or self.query.to_date

    def get_total_days(self):
        """Return total days of itinerary or fallback to Query's total_days"""
        if self.total_days:
            return self.total_days
        if self.travel_from and self.travel_to:
            return (self.travel_to - self.travel_from).days + 1
        if self.query.from_date and self.query.to_date:
            return (self.query.to_date - self.query.from_date).days + 1
        return self.query.total_days

    def adult(self):
        """Return itinerary adults or fallback to Query's adult"""
        return self.adults if self.adults is not None else self.query.adult

    def children(self):
        """Return itinerary childrens or fallback to Query's childrens"""
        return self.childrens if self.childrens is not None else self.query.childrens

    def infant(self):
        """Return itinerary infants or fallback to Query's infant"""
        return self.infants if self.infants is not None else self.query.infant

    def destination_list(self):
        """Return comma-separated destinations names"""
        return ", ".join(str(dest.name) for dest in self.destinations.all())

    # ✅ RENAMED: Changed method name to avoid conflict with field
    def check_if_archived(self):
        """Check if itinerary is archived (moved to history)"""
        return self.status == 'archived'

    def is_active(self):
        """Check if itinerary is active (current proposal)"""
        return self.status not in ['archived', 'cancelled']

    def get_child_versions(self):
        """Get all versions created from editing this itinerary"""
        return self.versions.filter(status__in=['draft', 'quoted', 'confirmed'])

    def get_active_version(self):
        """Get the active/current version of this itinerary (if edited)"""
        if self.parent_itinerary:
            return None  # This is a child version
        # Check if this itinerary has any active child versions
        active_child = self.versions.filter(
            status__in=['draft', 'quoted', 'confirmed']
        ).first()
        return active_child if active_child else self

    def __str__(self):
        return f"{self.name} (V{self.version_number})"

# models.py

class ItineraryDayPlan(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='day_plans')
    day_number = models.PositiveIntegerField()

    title = models.CharField(max_length=255, help_text="e.g., 'Cochin to Munnar (135 Km, 3.00 Hrs)'")
    description = models.TextField(help_text="Full day description")
    image = models.ImageField(upload_to='day_plan_images/', blank=True, null=True, help_text="Day illustration image")

    destination = models.ForeignKey(Destinations, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)


    hotels = models.ManyToManyField(Hotel, blank=True)
    houseboats = models.ManyToManyField(Houseboat, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    meal_plans = models.ManyToManyField(MealPlan, blank=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    inclusions = models.ManyToManyField(SpecialInclusion, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('itinerary', 'day_number')
        ordering = ['day_number']

    def get_image(self):
        """Returns custom image if set, otherwise destination default"""
        if self.image:
            return self.image
        elif self.destination and self.destination.default_image:
            return self.destination.default_image
        return None

    def get_description(self):
        """Returns custom description if set, otherwise destination default"""
        if self.description:
            return self.description
        elif self.destination and self.destination.default_description:
            return self.destination.default_description
        return ""

    def __str__(self):
        return f"{self.itinerary.name} - Day {self.day_number}"

import json
from django.db import models
from django.contrib.auth.models import User



class HotelBooking(models.Model):
    itinerary = models.ForeignKey(
        'Itinerary',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    custom_hotel_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="For Demo Hotels not in the database"
    )
    day_plan = models.ForeignKey(
        'ItineraryDayPlan',
        on_delete=models.CASCADE,
        related_name="hotel_bookings",
        null=True,
        blank=True
    )


    package_template = models.ForeignKey(
        'PackageTemplate',
        on_delete=models.CASCADE,
        related_name='hotel_bookings',
        null=True,
        blank=True
    )
    package_day_plan = models.ForeignKey(
        'PackageTemplateDayPlan',
        on_delete=models.CASCADE,
        related_name='hotel_bookings',
        null=True,
        blank=True
    )

    destination = models.ForeignKey('Destinations', on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50)
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True, blank=True)
    custom_room_type = models.CharField(max_length=100, null=True, blank=True, help_text="For manually typed room types")
    meal_plan = models.ForeignKey('MealPlan', on_delete=models.SET_NULL, null=True, blank=True)

    OPTION_CHOICES = [
            ('option_1', 'Standard'),
            ('option_2', 'Deluxe'),
            ('option_3', 'Premium'),
            ('option_4', 'Luxury'),

        ]
    option = models.CharField(max_length=10, choices=OPTION_CHOICES)

    num_rooms = models.PositiveIntegerField(default=0)
    num_double_beds = models.PositiveIntegerField(default=0)
    child_with_bed = models.PositiveIntegerField(default=0)
    child_without_bed = models.PositiveIntegerField(default=0)
    extra_beds = models.PositiveIntegerField(default=0)

    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_type = models.CharField(max_length=10, choices=[('fixed', 'Fixed'), ('percentage', 'Percentage')], default='fixed')
    markup_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custom_double_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_extra_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_child_with_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_child_without_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(itinerary__isnull=False, package_template__isnull=True) |
                    models.Q(itinerary__isnull=True, package_template__isnull=False)
                ),
                name='hotel_booking_itinerary_or_package'
            )
        ]

    def __str__(self):
        if self.hotel:
            return self.hotel.name
        return f"HotelBooking #{self.id}"

    @property
    def is_package_booking(self):
        return self.package_template is not None

    def get_total_inclusion_price(self):
        """Calculate total price of all special inclusions"""
        return sum(item.price for item in self.inclusion_items.all())

    def get_inclusions_summary(self):
        """Human-readable summary of all special inclusions"""
        if not self.inclusion_items.exists():
            return "No special inclusions"

        summaries = []
        for item in self.inclusion_items.all():
            parts = []
            if item.num_adults > 0:
                parts.append(f"{item.num_adults}A")
            if item.num_children > 0:
                parts.append(f"{item.num_children}C")
            people_text = "+".join(parts) if parts else "0"
            summaries.append(f"{item.special_inclusion.name} ({people_text}): ₹{item.price}")

        return " | ".join(summaries)

    def save(self, *args, **kwargs):
        """Auto-calculate num_rooms from num_double_beds (1:1 mapping)"""
        self.num_rooms = self.num_double_beds
        super().save(*args, **kwargs)

    def get_inclusions_json(self):
        """Return inclusions as JSON string for JavaScript"""
        inclusions_list = []
        for item in self.inclusion_items.all():
            inclusions_list.append({
                'id': item.special_inclusion.id,
                'adults': item.num_adults,
                'children': item.num_children
            })
        return json.dumps(inclusions_list)



class StandaloneInclusionBooking(models.Model):
    """
    For booking general/standalone inclusions like:
    - Mountain Climbing Expedition
    - Sunrise Trek Package
    - Zipline Adventure
    - Camping Night Under the Stars
    - Drone Photography Add-on
    """

    # Link to itinerary/package (same as HotelBooking)
    itinerary = models.ForeignKey(
        'Itinerary',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='standalone_inclusions'
    )
    day_plan = models.ForeignKey(
        'ItineraryDayPlan',
        on_delete=models.CASCADE,
        related_name="standalone_inclusions",
        null=True,
        blank=True
    )

    package_template = models.ForeignKey(
        'PackageTemplate',
        on_delete=models.CASCADE,
        related_name='standalone_inclusions',
        null=True,
        blank=True
    )
    package_day_plan = models.ForeignKey(
        'PackageTemplateDayPlan',
        on_delete=models.CASCADE,
        related_name='standalone_inclusions',
        null=True,
        blank=True
    )

    # The standalone inclusion being booked
    special_inclusion = models.ForeignKey(
        'SpecialInclusion',
        on_delete=models.CASCADE,
        limit_choices_to={'inclusion_type': 'general'},
        help_text="Only general/standalone inclusions can be booked"
    )

    # Booking details
    booking_date = models.DateField(
        help_text="Date when this activity/service is scheduled"
    )
    booking_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Scheduled time for the activity"
    )

    # Participant counts
    num_adults = models.PositiveIntegerField(
        default=1,
        help_text="Number of adults participating"
    )
    num_children = models.PositiveIntegerField(
        default=0,
        help_text="Number of children participating"
    )

    # Pricing breakdown
    adult_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per adult at time of booking"
    )
    child_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price per child at time of booking"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total before markup"
    )

    # Markup (same as HotelBooking)
    markup_type = models.CharField(
        max_length=10,
        choices=[('fixed', 'Fixed'), ('percentage', 'Percentage')],
        default='fixed'
    )
    markup_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    markup_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Final price after markup"
    )

    # Additional info
    notes = models.TextField(
        blank=True,
        help_text="Special instructions or notes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'TeamMember',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['booking_date', 'booking_time']
        verbose_name = "Standalone Inclusion Booking"
        verbose_name_plural = "Standalone Inclusion Bookings"
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(itinerary__isnull=False, package_template__isnull=True) |
                    models.Q(itinerary__isnull=True, package_template__isnull=False)
                ),
                name='standalone_inclusion_itinerary_or_package'
            )
        ]

    def __str__(self):
        return f"{self.special_inclusion.name} - {self.booking_date}"

    def calculate_prices(self):
        """Auto-calculate all prices based on special inclusion pricing"""
        inclusion = self.special_inclusion

        # Get prices from SpecialInclusion model
        self.adult_unit_price = inclusion.adult_price
        self.child_unit_price = inclusion.get_child_price()

        # Calculate subtotal
        adult_total = self.num_adults * self.adult_unit_price
        child_total = self.num_children * self.child_unit_price
        self.subtotal = adult_total + child_total

        # Calculate markup
        if self.markup_type == 'percentage':
            self.markup_amount = (self.subtotal * self.markup_value) / 100
        else:
            self.markup_amount = self.markup_value

        # Calculate final total
        self.total_price = self.subtotal + self.markup_amount

    def save(self, *args, **kwargs):
        """Auto-calculate prices before saving"""
        # ✅ FIXED: Only auto-calculate if update_fields is not specified
        # This allows manual updates from the pricing view
        update_fields = kwargs.get('update_fields')

        if update_fields is None:
            # Full save - recalculate everything
            self.calculate_prices()
        else:
            # Partial save from view - only recalculate if needed
            if 'markup_type' in update_fields or 'markup_value' in update_fields:
                # Recalculate markup and total when markup fields change
                if self.markup_type == 'percentage':
                    self.markup_amount = (self.subtotal * self.markup_value) / 100
                else:
                    self.markup_amount = self.markup_value

                self.total_price = self.subtotal + self.markup_amount

        super().save(*args, **kwargs)

    @property
    def is_package_booking(self):
        return self.package_template is not None

    def get_pricing_summary(self):
        """Human-readable pricing breakdown"""
        parts = []
        if self.num_adults > 0:
            parts.append(f"{self.num_adults} Adults × ₹{self.adult_unit_price} = ₹{self.num_adults * self.adult_unit_price}")
        if self.num_children > 0:
            parts.append(f"{self.num_children} Children × ₹{self.child_unit_price} = ₹{self.num_children * self.child_unit_price}")

        summary = " + ".join(parts)
        if self.markup_amount > 0:
            summary += f" + Markup ₹{self.markup_amount}"
        summary += f" = Total: ₹{self.total_price}"

        return summary

class ActivityBooking(models.Model):
    # ✅ FIXED - Made nullable and fixed related_name
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    day_plan = models.ForeignKey(
        ItineraryDayPlan,
        on_delete=models.CASCADE,
        related_name='activity_bookings',
        null=True,
        blank=True
    )

    # ✅ FIXED - Correct related_name
    package_template = models.ForeignKey(
        'PackageTemplate',
        on_delete=models.CASCADE,
        related_name='activity_bookings',  # ✅ FIXED
        null=True,
        blank=True
    )
    package_day_plan = models.ForeignKey(
        'PackageTemplateDayPlan',
        on_delete=models.CASCADE,
        related_name='activity_bookings',  # ✅ FIXED
        null=True,
        blank=True
    )

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)

    confirmation_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_type = models.CharField(max_length=10, choices=Itinerary.MARKUP_TYPE_CHOICES, default='fixed')
    markup_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custom_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(itinerary__isnull=False, package_template__isnull=True) |
                    models.Q(itinerary__isnull=True, package_template__isnull=False)
                ),
                name='activity_booking_itinerary_or_package'
            )
        ]

    @property
    def is_package_booking(self):
        return self.package_template is not None


class VehicleBooking(models.Model):
    # ✅ FIXED - Made nullable
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    day_plan = models.ForeignKey(
        ItineraryDayPlan,
        on_delete=models.CASCADE,
        related_name='vehicle_bookings',
        null=True,
        blank=True  # ✅ ADDED
    )

    # ✅ CORRECT - Already good
    package_template = models.ForeignKey(
        'PackageTemplate',
        on_delete=models.CASCADE,
        related_name='vehicle_bookings',
        null=True,
        blank=True
    )
    package_day_plan = models.ForeignKey(
        'PackageTemplateDayPlan',
        on_delete=models.CASCADE,
        related_name='vehicle_bookings',
        null=True,
        blank=True
    )

    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)

    total_km = models.PositiveIntegerField(default=0, help_text="Total kilometers for this booking")
    num_passengers = models.IntegerField()
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    option = models.CharField(max_length=50, null=True, blank=True)

    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_type = models.CharField(max_length=10, choices=Itinerary.MARKUP_TYPE_CHOICES, default='fixed')
    markup_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custom_total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(itinerary__isnull=False, package_template__isnull=True) |
                    models.Q(itinerary__isnull=True, package_template__isnull=False)
                ),
                name='vehicle_booking_itinerary_or_package'
            )
        ]

    @property
    def is_package_booking(self):
        return self.package_template is not None

class HouseboatBooking(models.Model):
    # Foreign Keys - Itinerary or Package Template (one must be set)
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    day_plan = models.ForeignKey(
        ItineraryDayPlan,
        on_delete=models.CASCADE,
        related_name='houseboat_bookings',
        null=True,
        blank=True
    )

    package_template = models.ForeignKey(
        'PackageTemplate',
        on_delete=models.CASCADE,
        related_name='houseboat_bookings',
        null=True,
        blank=True
    )
    package_day_plan = models.ForeignKey(
        'PackageTemplateDayPlan',
        on_delete=models.CASCADE,
        related_name='houseboat_bookings',
        null=True,
        blank=True
    )

    # Booking Details
    houseboat = models.ForeignKey(Houseboat, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    OPTION_CHOICES = [
        ('option1', 'Standard'),
        ('option2', 'Deluxe'),
        ('option3', 'Premium'),
        ('option4', 'Luxury'),
    ]
    option = models.CharField(
        max_length=10,
        choices=OPTION_CHOICES,
        default='option1',
        help_text="Pricing option for this houseboat"
    )
    # Room Configuration
    num_one_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 1-Bed Rooms")
    num_two_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 2-Bed Rooms")
    num_three_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 3-Bed Rooms")
    num_four_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 4-Bed Rooms")
    num_five_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 5-Bed Rooms")
    num_six_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 6-Bed Rooms")
    num_seven_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 7-Bed Rooms")
    num_eight_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 8-Bed Rooms")
    num_nine_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 9-Bed Rooms")
    num_ten_bed_rooms = models.PositiveIntegerField(default=0, verbose_name="Number of 10-Bed Rooms")
    num_extra_beds = models.PositiveIntegerField(default=0, verbose_name="Number of Extra Beds")

    # Pricing Fields
    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_type = models.CharField(max_length=10, choices=Itinerary.MARKUP_TYPE_CHOICES, default='fixed')
    markup_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Custom Pricing Overrides
    custom_one_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_two_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_three_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_four_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_five_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_six_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_seven_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_eight_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_nine_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_ten_bed_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_extra_bed_hb_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(itinerary__isnull=False, package_template__isnull=True) |
                    models.Q(itinerary__isnull=True, package_template__isnull=False)
                ),
                name='houseboat_booking_itinerary_or_package'
            )
        ]

    def __str__(self):
        if self.houseboat:
            return f"{self.houseboat.name} - {self.check_in_date}"
        return f"HouseboatBooking #{self.id}"

    # ✅ NEW: Properties for booking type
    @property
    def is_package_booking(self):
        """Check if this belongs to a package template"""
        return self.package_template_id is not None

    @property
    def is_itinerary_booking(self):
        """Check if this belongs to an itinerary"""
        return self.itinerary_id is not None

    # ✅ NEW: Multi-inclusion helper methods
    def get_total_inclusion_price(self):
        """Calculate total price of all special inclusions"""
        return sum(item.price for item in self.inclusion_items.all())

    def get_inclusions_summary(self):
        """Human-readable summary of all special inclusions"""
        if not self.inclusion_items.exists():
            return "No special inclusions"

        summaries = []
        for item in self.inclusion_items.all():
            parts = []
            if item.num_adults > 0:
                parts.append(f"{item.num_adults}A")
            if item.num_children > 0:
                parts.append(f"{item.num_children}C")
            people_text = "+".join(parts) if parts else "0"
            summaries.append(f"{item.special_inclusion.name} ({people_text}): ₹{item.price}")

        return " | ".join(summaries)

    def get_inclusions_json(self):
        """Return inclusions as JSON string for JavaScript"""
        import json
        inclusions_list = []
        for item in self.inclusion_items.all():
            inclusions_list.append({
                'id': item.special_inclusion.id,
                'adults': item.num_adults,
                'children': item.num_children,
                'price': float(item.price)
            })
        return json.dumps(inclusions_list)

    # ✅ NEW: Calculate total rooms
    def get_total_rooms(self):
        """Calculate total number of rooms booked"""
        return (
            self.num_one_bed_rooms +
            self.num_two_bed_rooms +
            self.num_three_bed_rooms +
            self.num_four_bed_rooms +
            self.num_five_bed_rooms +
            self.num_six_bed_rooms +
            self.num_seven_bed_rooms +
            self.num_eight_bed_rooms +
            self.num_nine_bed_rooms +
            self.num_ten_bed_rooms
        )



class HouseboatBookingInclusion(models.Model):
    """
    Model to track multiple special inclusions per houseboat booking.
    Each inclusion can have different adult/child counts and pricing.
    """
    houseboat_booking = models.ForeignKey(
        'HouseboatBooking',
        on_delete=models.CASCADE,
        related_name='inclusion_items'
    )
    special_inclusion = models.ForeignKey(
        'SpecialInclusion',
        on_delete=models.CASCADE
    )
    num_adults = models.PositiveIntegerField(
        default=0,
        verbose_name="Adults with this Inclusion"
    )
    num_children = models.PositiveIntegerField(
        default=0,
        verbose_name="Children with this Inclusion"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total Price for this Inclusion Item"
    )

    class Meta:
        verbose_name = "Houseboat Booking Inclusion"
        verbose_name_plural = "Houseboat Booking Inclusions"
        ordering = ['id']

    def __str__(self):
        type_badge = "[PKG]" if self.is_package_booking else "[ITN]"
        return f"{type_badge} {self.special_inclusion.name} - {self.num_adults}A + {self.num_children}C (₹{self.price})"

    # Properties to determine booking type via HouseboatBooking
    @property
    def is_package_booking(self):
        """Check if this belongs to a package template booking"""
        return self.houseboat_booking.package_template_id is not None

    @property
    def is_itinerary_booking(self):
        """Check if this belongs to an itinerary booking"""
        return self.houseboat_booking.itinerary_id is not None

    @property
    def booking_type(self):
        """Get the booking type as a string"""
        if self.is_package_booking:
            return 'package'
        elif self.is_itinerary_booking:
            return 'itinerary'
        return 'unknown'

    @property
    def parent_name(self):
        """Get the name of the parent (package or itinerary)"""
        if self.is_package_booking:
            return self.houseboat_booking.package_template.name
        elif self.is_itinerary_booking:
            return self.houseboat_booking.itinerary.name
        return "Unknown"

    def calculate_price(self):
        """Calculate price based on adults, children, and inclusion pricing"""
        from decimal import Decimal

        if not self.special_inclusion:
            return Decimal('0.00')

        inclusion = self.special_inclusion

        if inclusion.pricing_type == 'free':
            return Decimal('0.00')

        if inclusion.pricing_type == 'per_booking':
            return inclusion.adult_price

        if inclusion.pricing_type == 'per_room':
            # Calculate total rooms for houseboat
            total_rooms = self.houseboat_booking.get_total_rooms()
            return inclusion.adult_price * (total_rooms or 1)

        if inclusion.pricing_type == 'per_person':
            adult_price = inclusion.adult_price * self.num_adults
            child_price = inclusion.get_child_price() * self.num_children
            return adult_price + child_price

        return Decimal('0.00')

    def save(self, *args, **kwargs):
        """Auto-calculate price before saving"""
        self.price = self.calculate_price()
        super().save(*args, **kwargs)



# Add to your models.py
class ItineraryPricingOption(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='pricing_options')
    option_name = models.CharField(max_length=50)  # "Option 1", "Option 2", etc.
    option_number = models.PositiveIntegerField()  # 1, 2, 3, etc.

    vehicle_type = models.CharField(max_length=100, default="A/C Ertiga", help_text="Type of vehicle")
    number_of_rooms = models.PositiveIntegerField(default=1)
    extra_beds = models.PositiveIntegerField(default=0)
    child_without_bed = models.PositiveIntegerField(default=0)
    child_with_bed = models.PositiveIntegerField(default=0)
    child_ages = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., '5, 8, 12'")

    # Pricing details
    net_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Tax calculations
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Hotel breakdown for this option
    hotels_included = models.JSONField(default=list)  # Store hotel names/ids for this option

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('itinerary', 'option_number')
        ordering = ['option_number']

    def __str__(self):
        return f"{self.itinerary.name} - {self.option_name}: ₹{self.final_amount}"


from decimal import Decimal
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class PackageTemplate(models.Model):
    # Basic Information
    name = models.CharField(max_length=255, help_text="Package name (e.g., 'Kerala Backwaters 5 Days')")
    description = models.TextField(blank=True, null=True, help_text="Package overview and highlights")

    # Link to existing theme
    theme = models.ForeignKey('PackageTheme', on_delete=models.SET_NULL, null=True, blank=True)
    from_date = models.DateField(
        null=True,
        blank=True,
        help_text="Package travel start date (when the trip begins)",
        verbose_name="Travel From Date"
    )
    to_date = models.DateField(
        null=True,
        blank=True,
        help_text="Package travel end date (when the trip ends)",
        verbose_name="Travel To Date"
    )
        # ✅ Optional: Seasonal Availability (not required)
    available_from = models.DateField(
        null=True,
        blank=True,
        help_text="Package available from this date (optional)"
    )
    available_until = models.DateField(
        null=True,
        blank=True,
        help_text="Package available until this date (optional)"
    )
    # Package Duration & Pax
    total_days = models.PositiveIntegerField(help_text="Total number of days")
    default_adults = models.PositiveIntegerField(default=2, help_text="Default number of adults")
    default_children = models.PositiveIntegerField(default=0, help_text="Default number of children")
    default_infants = models.PositiveIntegerField(default=0, help_text="Default number of infants")

    # Destinations
    destinations = models.ManyToManyField('Destinations', help_text="Destinations covered in this package")

    # Notes
    notes = models.TextField(blank=True, null=True, help_text="Package notes and additional information")


    # ✅ ADD THESE TAX & DISCOUNT FIELDS
    cgst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('2.5'),
        help_text="CGST percentage (e.g., 2.5 for 2.5%)"
    )

    sgst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('2.5'),
        help_text="SGST percentage (e.g., 2.5 for 2.5%)"
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Flat discount amount (not percentage)"
    )

    # Visual & Marketing
    thumbnail = models.ImageField(
        upload_to='package_templates/',
        blank=True,
        null=True,
        help_text="Package thumbnail image"
    )
    cover_image = models.ImageField(
        upload_to='package_templates/covers/',
        blank=True,
        null=True,
        help_text="Cover image for package display"
    )

    # Package highlights (rich text)
    highlights = RichTextField(
        blank=True,
        null=True,
        verbose_name="Package Highlights",
        help_text="Key features and highlights of this package"
    )

    # Status & Metadata
    is_active = models.BooleanField(default=True, help_text="Is this package template available for use?")
    is_featured = models.BooleanField(default=False, help_text="Show in featured/recommended packages")
    is_finalized = models.BooleanField(default=False, help_text="Has pricing been finalized?")
    finalized_at = models.DateTimeField(null=True, blank=True, help_text="When pricing was finalized")

    # Usage tracking
    times_used = models.PositiveIntegerField(default=0, help_text="Number of times this package was inserted")
    last_used = models.DateTimeField(null=True, blank=True, help_text="Last time this package was used")

    # Metadata
    created_by = models.ForeignKey('TeamMember', on_delete=models.SET_NULL, null=True, related_name='created_packages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & Tags
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Comma-separated tags (e.g., honeymoon, family, adventure)"
    )

    class Meta:
        ordering = ['-is_featured', '-times_used', '-created_at']
        verbose_name = "Package Template"
        verbose_name_plural = "Package Templates"
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['-times_used']),
        ]


    # ✅ ADD THIS PROPERTY
    @property
    def nights(self):
        """Calculate nights from total_days"""
        return self.total_days - 1 if self.total_days > 0 else 0

    def destination_list(self):
        """Returns comma-separated list of destinations"""
        return ", ".join([dest.name for dest in self.destinations.all()])

    def increment_usage(self):
        """Increment usage counter and update last_used timestamp"""
        self.times_used += 1
        self.last_used = timezone.now()
        self.save(update_fields=['times_used', 'last_used'])

    def __str__(self):
        return f"{self.name} ({self.total_days} Days)"

    def date_range_display(self):
        """Returns formatted date range string"""
        if self.from_date and self.to_date:
            return f"{self.from_date.strftime('%d %b %Y')} to {self.to_date.strftime('%d %b %Y')}"
        elif self.from_date:
            return f"From {self.from_date.strftime('%d %b %Y')}"
        elif self.to_date:
            return f"Until {self.to_date.strftime('%d %b %Y')}"
        return "Dates not set"

    def calculated_total_days(self):
        """Calculate total days from from_date and to_date if both are set"""
        if self.from_date and self.to_date:
            delta = self.to_date - self.from_date
            return delta.days + 1  # +1 because both start and end dates are inclusive
        return self.total_days

    @property
    def default_pricing(self):
        """Get the first pricing option"""
        return self.pricing_options.first()

    @property
    def total_package_price(self):
        """Get total package price from first pricing option"""
        default_pricing = self.default_pricing
        if default_pricing:
            return default_pricing.final_amount
        return Decimal('0.00')

    @property
    def total_passengers(self):
        """Calculate total passengers (adults + children + infants)"""
        return self.default_adults + self.default_children + self.default_infants




class PackageTemplateDayPlan(models.Model):
    """
    Day-by-day plan for package templates.
    Similar to ItineraryDayPlan but for reusable templates.
    """

    package_template = models.ForeignKey(
        PackageTemplate,
        on_delete=models.CASCADE,
        related_name='day_plans'
    )
    day_number = models.PositiveIntegerField()

    # Day details
    title = models.CharField(
        max_length=255,
        help_text="e.g., 'Cochin to Munnar (135 Km, 3.00 Hrs)'"
    )
    description = models.TextField(help_text="Detailed day description")

    # Visual
    image = models.ImageField(
        upload_to='package_day_images/',
        blank=True,
        null=True,
        help_text="Day illustration image"
    )

    # Location
    destination = models.ForeignKey(
        Destinations,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Travel info (optional)
    distance_km = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Distance to travel this day (in km)"
    )
    travel_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Approximate travel time (in hours)"
    )

    # Additional notes
    notes = models.TextField(blank=True, null=True, help_text="Internal notes for this day")

    # Suggested resources (ManyToMany - these will be copied to actual itinerary)
    hotels = models.ManyToManyField(Hotel, blank=True, help_text="Suggested hotels for this day")
    houseboats = models.ManyToManyField(Houseboat, blank=True, help_text="Suggested houseboats")
    activities = models.ManyToManyField(Activity, blank=True, help_text="Suggested activities")
    meal_plans = models.ManyToManyField(MealPlan, blank=True, help_text="Suggested meal plans")
    vehicles = models.ManyToManyField(Vehicle, blank=True, help_text="Suggested vehicles")
    general_inclusions = models.ManyToManyField(
        'SpecialInclusion',
        blank=True,
        limit_choices_to={'inclusion_type': 'general'},
        related_name='package_day_plans'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('package_template', 'day_number')
        ordering = ['day_number']
        verbose_name = "Package Day Plan"
        verbose_name_plural = "Package Day Plans"

    def get_image(self):
        """Returns custom image if set, otherwise destination default"""
        if self.image:
            return self.image
        elif self.destination and self.destination.default_image:
            return self.destination.default_image
        return None

    def get_description(self):
        """Returns custom description if set, otherwise destination default"""
        if self.description:
            return self.description
        elif self.destination and self.destination.default_description:
            return self.destination.default_description
        return ""

    def __str__(self):
        return f"{self.package_template.name} - Day {self.day_number}: {self.title}"


class PackageTemplateCategory(models.Model):
    """
    Categories for organizing package templates.
    E.g., Honeymoon, Family, Adventure, Budget, Luxury, etc.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Font Awesome icon class (e.g., 'fa-heart' for honeymoon)"
    )
    color_code = models.CharField(
        max_length=7,
        default='#007bff',
        help_text="Hex color code for category badge"
    )

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Sort order for display")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Package Category"
        verbose_name_plural = "Package Categories"

    def __str__(self):
        return self.name


class PackagePricingOption(models.Model):
    package_template = models.ForeignKey(
        PackageTemplate,
        on_delete=models.CASCADE,
        related_name='pricing_options'
    )
    option_name = models.CharField(max_length=50)
    option_number = models.PositiveIntegerField()  # ✅ Changed to PositiveIntegerField

    # ✅ ADD BOOKING DETAILS
    vehicle_type = models.CharField(max_length=100, default="A/C Ertiga", help_text="Type of vehicle")
    number_of_rooms = models.PositiveIntegerField(default=1)
    extra_beds = models.PositiveIntegerField(default=0)
    child_without_bed = models.PositiveIntegerField(default=0)
    child_with_bed = models.PositiveIntegerField(default=0)
    child_ages = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., '5, 8, 12'")

    # Pricing breakdown
    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅ ADDED
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Store which hotels are included
    hotels_included = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['option_number']
        unique_together = ['package_template', 'option_number']

    def __str__(self):
        return f"{self.package_template.name} - {self.option_name}"





