from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(OrganisationalSetting)
admin.site.register(InvoiceTerms)
admin.site.register(PackageTerms)
admin.site.register(PackageTermss)
admin.site.register(BankInformation)
admin.site.register(Itinerary)
admin.site.register(TeamMember)
admin.site.register(HotelBooking)
admin.site.register(HotelBookingInclusion)
admin.site.register(HouseboatBookingInclusion)
admin.site.register(Hotel)
admin.site.register(MealPlan)
admin.site.register(VehicleBooking)
admin.site.register(ActivityBooking)
admin.site.register(HouseboatPrice)
admin.site.register(Hotelprice)
admin.site.register(PackagePricingOption)
admin.site.register(HouseboatBooking)
admin.site.register(ItineraryPricingOption)
admin.site.register(StandaloneInclusionBooking)
class HouseboatImageInline(admin.TabularInline):  # or StackedInline for bigger previews
    model = HouseboatImage
    extra = 1   # how many empty image forms to show
    fields = ['image']  # only show the image field


@admin.register(Houseboat)
class HouseboatAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'contact_person', 'status', 'created_at')
    list_filter = ('status', 'destination')
    search_fields = ('name', 'contact_person')
    inlines = [HouseboatImageInline]


@admin.register(HouseboatImage)
class HouseboatImageAdmin(admin.ModelAdmin):
    list_display = ('houseboat', 'image')
    
    
from django.contrib import admin
from .models import Destinations, ItineraryDayPlan

@admin.register(Destinations)
class DestinationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'has_default_image', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    
    # ✅ ADD THESE FIELDS TO ADMIN FORM
    fields = ['name', 'default_image', 'default_description', 'is_active']
    
    def has_default_image(self, obj):
        return bool(obj.default_image)
    has_default_image.boolean = True
    has_default_image.short_description = 'Has Image'

@admin.register(ItineraryDayPlan)
class ItineraryDayPlanAdmin(admin.ModelAdmin):
    list_display = ['itinerary', 'day_number', 'title', 'destination', 'has_custom_image']
    list_filter = ['itinerary', 'destination']
    search_fields = ['title', 'description']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('itinerary', 'day_number', 'destination', 'title')
        }),
        ('Content (Optional - Uses destination defaults if empty)', {
            'fields': ('description', 'image', 'notes'),
            'description': 'Leave empty to use destination defaults'
        }),
        ('Related Items', {
            'fields': ('hotels', 'vehicles', 'activities', 'houseboats', 'meal_plans', 'inclusions'),
            'classes': ('collapse',)
        }),
    )
    
    def has_custom_image(self, obj):
        return bool(obj.image)
    has_custom_image.boolean = True
    has_custom_image.short_description = 'Custom Image'


from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'supplier_type', 'full_name', 'email', 'mobile_no', 'is_active', 'is_verified', 'created_at')
    list_filter = ('supplier_type', 'is_active', 'is_verified', 'city', 'created_at')
    search_fields = ('company_name', 'email', 'mobile_no', 'supplier_first_name', 'supplier_last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'supplier_type', 'website', 'description')
        }),
        ('Contact Person', {
            'fields': ('supplier_first_name', 'supplier_last_name', 'email', 'mobile_no', 'phone_no')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Business Details', {
            'fields': ('gst_number', 'is_active', 'is_verified')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )



@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'vehicle_type', 
        'destination', 
        'capacity',
        'supplier', 
        'status', 
        'created_at'
    ]
    
    list_filter = [
        'vehicle_type', 
        'status', 
        'destination',
        'supplier',
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'registration_number',
        'supplier__company_name',
        'contact_person'
    ]
    
    autocomplete_fields = ['supplier']
    
    readonly_fields = [
        'created_at', 
        'supplier_name',
        'supplier_contact'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'vehicle_type', 'destination', 'status')
        }),
        ('Supplier Information', {
            'fields': ('supplier', 'supplier_name', 'supplier_contact')
        }),
        ('Details', {
            'fields': ('details', 'photo', 'capacity')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_phone', 'registration_number')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )