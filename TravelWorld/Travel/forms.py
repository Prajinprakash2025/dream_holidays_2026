from django import forms
from .models import *




from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'supplier_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'supplier_first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'supplier_last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'phone_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alternate phone'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Full address'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal code'
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GST number'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Business description'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_no'].required = False
        self.fields['state'].required = False
        self.fields['postal_code'].required = False
        self.fields['gst_number'].required = False
        self.fields['website'].required = False
        self.fields['description'].required = False
        self.fields['notes'].required = False

        
# forms.py

from django import forms
from .models import Destinations

class DestinationsForm(forms.ModelForm):
    class Meta:
        model = Destinations
        # ✅ Include all fields from the model
        fields = ['name', 'default_image', 'default_description', 'is_active']
        
        # ✅ Add widgets for styling and better UX
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter destination name',
                'required': True
            }),
            'default_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'default_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter default itinerary description for this destination'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 48px; height: 24px; cursor: pointer;'
            }),
        }
        
        # ✅ Customize labels
        labels = {
            'name': 'Destination Name',
            'default_image': 'Default Image',
            'default_description': 'Default Description',
            'is_active': 'Active Status',
        }
        
        # ✅ Add help text
        help_texts = {
            'name': 'Enter the name of the destination (e.g., Paris, Tokyo, Mumbai)',
            'default_image': 'Upload a default image for this destination (Optional)',
            'default_description': 'Default itinerary description for this destination (Optional)',
            'is_active': 'Enable this destination for use in itineraries',
        }

        
class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Room Type Name'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
        

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
        
class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['name', 'status']  # Exclude created_at (auto-generated)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Meal Plan Name'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
from django import forms
from .models import Hotel, Supplier, Destinations


class HotelForm(forms.ModelForm):
    """
    Form for creating and editing hotels with supplier assignment
    """
    
    class Meta:
        model = Hotel
        fields = [
            'name',
            'category',
            'destination',
            'supplier',
            'details',
            'contact_person',
            'phone_number',
            'email',
            'phone',
            'hotel_link',
            'image',
            'status'
        ]
        
        widgets = {
            # Basic Info
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hotel name',
                'id': 'id_name',
                'required': True
            }),
            
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_category',
                'required': True
            }),
            
            'destination': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_destination',
                'required': True
            }),
            
            'supplier': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_supplier'
            }),
            
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_details',
                'rows': 3,
                'placeholder': 'Enter hotel details, amenities, description'
            }),
            
            # Contact Information
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_contact_person',
                'placeholder': 'Contact person name',
                'required': True
            }),
            
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_phone_number',
                'placeholder': '+91 XXXXX XXXXX',
                'type': 'tel',
                'required': True
            }),
            
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_phone',
                'placeholder': '+91 XXXXX XXXXX (Optional)',
                'type': 'tel'
            }),
            
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'id_email',
                'placeholder': 'hotel@example.com',
                'required': True
            }),
            
            # Links & Media
            'hotel_link': forms.URLInput(attrs={
                'class': 'form-control',
                'id': 'id_hotel_link',
                'placeholder': 'https://www.example.com',
                'type': 'url'
            }),
            
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_image',
                'accept': 'image/*'
            }),
            
            # Status
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_status'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        
        # ✅ FIXED: Filter suppliers to only show hotel suppliers that are active
        self.fields['supplier'].queryset = Supplier.objects.filter(
            supplier_type='hotel',
            is_active=True
        ).order_by('company_name')
        
        self.fields['supplier'].required = False
        self.fields['supplier'].empty_label = "Select Supplier (Optional)"
        
        # ✅ Filter destinations to only show active ones
        self.fields['destination'].queryset = Destinations.objects.filter(
            is_active=True
        ).order_by('name')
        
        # Set initial status value
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
        else:
            self.fields['status'].initial = True
    
    def clean(self):
        """
        Validate form data
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        # Check if hotel with same email already exists (excluding current instance)
        if email:
            existing = Hotel.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                self.add_error('email', 'A hotel with this email already exists.')
        
        # Validate phone numbers
        phone_number = cleaned_data.get('phone_number')
        phone = cleaned_data.get('phone')
        
        if phone_number:
            cleaned_phone = phone_number.replace('+', '').replace('-', '').replace(' ', '')
            if not cleaned_phone.isdigit():
                self.add_error('phone_number', 'Enter a valid phone number.')
        
        if phone:
            cleaned_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
            if not cleaned_phone.isdigit():
                self.add_error('phone', 'Enter a valid phone number.')
        
        return cleaned_data


class HotelFilterForm(forms.Form):
    """
    Form for filtering hotels
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search hotels...'
        })
    )
    
    category = forms.MultipleChoiceField(
        required=False,
        choices=Hotel.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    destination = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Destinations.objects.filter(is_active=True).order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    supplier = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Supplier.objects.filter(
            supplier_type='hotel',  # ✅ Only hotel suppliers
            is_active=True
        ).order_by('company_name'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('true', 'Active'),
            ('false', 'Inactive'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )




class HotelPriceForm(forms.ModelForm):
    class Meta:
        model = Hotelprice
        fields = ['from_date', 'to_date', 'room_type', 'meal_plan', 'double_bed', 'child_without_bed', 'child_with_bed', 'extra_bed']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'meal_plan': forms.Select(attrs={'class': 'form-control'}),
            'double_bed': forms.NumberInput(attrs={'class': 'form-control'}),
            'child_without_bed': forms.NumberInput(attrs={'class': 'form-control'}),
            'child_with_bed': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_bed': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        



from django import forms
from .models import Houseboat, Supplier, Destinations, HouseboatImage


class HouseboatForm(forms.ModelForm):
    """
    Form for creating and editing houseboats with supplier assignment
    """
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(
            supplier_type='houseboat',
            is_active=True
        ),
        required=False,
        empty_label="Select Supplier (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_supplier'
        })
    )
    
    destination = forms.ModelChoiceField(
        queryset=Destinations.objects.all(),
        required=True,  # ✅ Make destination required
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_destination'
        })
    )
    
    class Meta:
        model = Houseboat
        fields = [
            'name',
            'houseboat_type',
            'destination',
            'supplier',
            'num_cabins',
            'num_bathrooms',
            'total_capacity',
            'length_meters',
            'details',
            'amenities',
            'special_features',
            'contact_person',
            'phone_number',
            'phone_alternate',
            'email',
            'website',
            'registration_number',
            'image',  # Keep for single image upload
            'is_premium',
            'maximum_stay_days',
            'status'
        ]
        # ✅ IMPORTANT: Exclude auto-populated fields
        exclude = ['created_by', 'created_by_username']
        
        widgets = {
            # Basic Information
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter houseboat name',
                'autocomplete': 'off'
            }),
            
            'houseboat_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter houseboat details and description',
                'autocomplete': 'off'
            }),
            
            # Specifications
            'num_cabins': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of cabins',
                'autocomplete': 'off'
            }),
            
            'num_bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of bathrooms',
                'autocomplete': 'off'
            }),
            
            'total_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Total capacity (guests)',
                'autocomplete': 'off'
            }),
            
            'length_meters': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '1',
                'placeholder': 'Length in meters',
                'autocomplete': 'off'
            }),
            
            'maximum_stay_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Maximum stay days',
                'autocomplete': 'off'
            }),
            
            # Amenities & Features
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Air Conditioning, Hot Water, WiFi, Kitchen, Swimming Pool',
                'autocomplete': 'off'
            }),
            
            'special_features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Rooftop Deck, Spa, Restaurant, Water Sports',
                'autocomplete': 'off'
            }),
            
            # Contact Information
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name',
                'autocomplete': 'name'
            }),
            
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX',
                'type': 'tel',
                'autocomplete': 'tel'
            }),
            
            'phone_alternate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX (Optional)',
                'type': 'tel',
                'autocomplete': 'tel'
            }),
            
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'houseboat@example.com',
                'autocomplete': 'email'
            }),
            
            # Links & Media
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com',
                'type': 'url',
                'autocomplete': 'url'
            }),
            
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Registration/License number',
                'autocomplete': 'off'
            }),
            
            # Status
            'is_premium': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_premium',
                'style': 'width: 48px; height: 24px; cursor: pointer;'
            }),
            
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_status',
                'style': 'width: 48px; height: 24px; cursor: pointer;'
            }),
        }
    
    def clean(self):
        """
        Validate form data
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        num_cabins = cleaned_data.get('num_cabins')
        total_capacity = cleaned_data.get('total_capacity')
        
        # Check if email already exists
        if email:
            existing = Houseboat.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                self.add_error('email', 'A houseboat with this email already exists.')
        
        # Validate capacity vs cabins
        if num_cabins and total_capacity:
            if total_capacity < num_cabins:
                self.add_error('total_capacity', 
                    'Total capacity must be at least equal to number of cabins.')
        
        # Validate phone numbers
        phone_number = cleaned_data.get('phone_number')
        phone_alternate = cleaned_data.get('phone_alternate')
        
        if phone_number and not phone_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            self.add_error('phone_number', 'Enter a valid phone number.')
        
        if phone_alternate and not phone_alternate.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            self.add_error('phone_alternate', 'Enter a valid phone number.')
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(HouseboatForm, self).__init__(*args, **kwargs)
        
        # ✅ Set required fields
        required_fields = [
            'name', 'houseboat_type', 'destination', 
            'contact_person', 'phone_number', 'email',
            'num_cabins', 'total_capacity', 'details'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        
        # Set initial status values
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
            self.fields['is_premium'].initial = self.instance.is_premium
        else:
            self.fields['status'].initial = True
            self.fields['is_premium'].initial = False


class HouseboatFilterForm(forms.Form):
    """
    Form for filtering houseboats
    """
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search houseboats...',
            'autocomplete': 'off'
        })
    )
    
    houseboat_type = forms.MultipleChoiceField(
        required=False,
        choices=Houseboat.HOUSEBOAT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    destination = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Destinations.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    supplier = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Supplier.objects.filter(
            supplier_type='houseboat',
            is_active=True
        ),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    min_capacity = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum capacity',
            'autocomplete': 'off'
        })
    )
    
    is_premium = forms.NullBooleanField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }, choices=[
            (None, 'All'),
            (True, 'Premium Only'),
            (False, 'Standard Only'),
        ])
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('true', 'Active'),
            ('false', 'Inactive'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class HouseboatImageForm(forms.ModelForm):
    class Meta:
        model = HouseboatImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

from django.forms import modelformset_factory

HouseboatImageFormSet = modelformset_factory(
    HouseboatImage,
    form=HouseboatImageForm,
    extra=3,  # Show 3 extra empty forms to upload new images
    can_delete=True  # Allow deleting existing images by adding a checkbox
)


class HouseboatPriceForm(forms.ModelForm):
    class Meta:
        model = HouseboatPrice
        exclude = ['houseboat']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        
        
class ActivityForm(forms.ModelForm):
    """
    Form for creating and editing activities with supplier assignment
    """
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(
            supplier_type='activity',
            is_active=True
        ),
        required=False,
        empty_label="Select Supplier (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_supplier'
        })
    )
    
    destination = forms.ModelChoiceField(
        queryset=Destinations.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_destination'
        })
    )
    
    class Meta:
        model = Activity
        fields = [
            'name',
            'activity_type',
            'destination',
            'supplier',
            'difficulty_level',
            'duration_hours',
            'max_participants',
            'min_participants',
            'details',
            'inclusions',
            'exclusions',
            'age_restriction',
            'meeting_point',
            'contact_person',
            'contact_phone',
            'website',
            'photo',
            'is_active'
        ]
        
        widgets = {
            # Basic Information
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter activity name',
                'required': True
            }),
            
            'activity_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            
            'difficulty_level': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter activity details and description',
                'required': True
            }),
            
            'inclusions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is included in this activity?'
            }),
            
            'exclusions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is not included?'
            }),
            
            # Participant Information
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0.5',
                'placeholder': 'Duration in hours'
            }),
            
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Maximum participants'
            }),
            
            'min_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Minimum participants'
            }),
            
            'age_restriction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Minimum 18 years, No age restriction'
            }),
            
            # Contact Information
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX',
                'type': 'tel'
            }),
            
            'meeting_point': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where do participants meet?'
            }),
            
            # Links & Media
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com',
                'type': 'url'
            }),
            
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            
            # Status
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_active'
            }),
        }
    
    def clean(self):
        """
        Validate form data
        """
        cleaned_data = super().clean()
        max_participants = cleaned_data.get('max_participants')
        min_participants = cleaned_data.get('min_participants')
        
        # Validate participant count
        if max_participants and min_participants:
            if min_participants > max_participants:
                self.add_error('min_participants', 
                    'Minimum participants cannot be greater than maximum.')
        
        # Validate duration
        duration = cleaned_data.get('duration_hours')
        if duration and duration <= 0:
            self.add_error('duration_hours', 'Duration must be greater than 0.')
        
        # Validate contact phone
        contact_phone = cleaned_data.get('contact_phone')
        if contact_phone and not contact_phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            self.add_error('contact_phone', 'Enter a valid phone number.')
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        
        # Set initial status value
        if self.instance.pk:
            self.fields['is_active'].initial = self.instance.is_active
        else:
            self.fields['is_active'].initial = True


class ActivityFilterForm(forms.Form):
    """
    Form for filtering activities
    """
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search activities...'
        })
    )
    
    activity_type = forms.MultipleChoiceField(
        required=False,
        choices=Activity.ACTIVITY_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    difficulty_level = forms.MultipleChoiceField(
        required=False,
        choices=Activity.DIFFICULTY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    destination = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Destinations.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    supplier = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Supplier.objects.filter(
            supplier_type='activity',
            is_active=True
        ),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('true', 'Active'),
            ('false', 'Inactive'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

class ActivityPriceForm(forms.ModelForm):
    class Meta:
        model = ActivityPrice
        fields = ['from_date', 'to_date', 'per_person']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'per_person': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
# forms.py
from django import forms
from .models import SpecialInclusion

class SpecialInclusionForm(forms.ModelForm):
    class Meta:
        model = SpecialInclusion
        fields = [
            'name', 'pricing_type', 'adult_price',
            'child_pricing_type', 'child_price_value',
            'min_age', 'max_age', 'details', 'photo', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Airport Transfer, Tour Guide'
            }),
            'pricing_type': forms.Select(attrs={'class': 'form-select'}),
            'adult_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'child_pricing_type': forms.Select(attrs={'class': 'form-select'}),
            'child_price_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'min_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'e.g., 3'
            }),
            'max_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'e.g., 12'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what this inclusion offers',
                'required': False  # ✅ Make it optional
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Make details field optional
        self.fields['details'].required = False
        self.fields['photo'].required = False
        self.fields['min_age'].required = False
        self.fields['max_age'].required = False



class InclusionPriceForm(forms.ModelForm):
    class Meta:
        model = InclusionPrice
        fields = ['from_date', 'to_date', 'per_person_price']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'per_person_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        

from django import forms
from .models import Vehicle, Supplier

class VehicleForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(
            supplier_type='vehicle',
            is_active=True
        ),
        required=False,
        empty_label="Select Supplier (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Vehicle
        fields = [
            'name',
            'vehicle_type',
            'destination',
            'capacity',
            'details',
            'registration_number',
            'contact_person',
            'contact_phone',
            'supplier',
            'photo',
            'status'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vehicle name'
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'destination': forms.Select(attrs={
                'class': 'form-control'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter capacity'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Vehicle details and description'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., KL-01-AB-1234'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Driver or contact person name'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }



from django import forms
from .models import StandaloneInclusionBooking, SpecialInclusion

class StandaloneInclusionBookingForm(forms.ModelForm):
    """
    Form for booking standalone inclusions (general activities/services)
    like Mountain Climbing, Zipline, Camping, Drone Photography, etc.
    """
    
    special_inclusion = forms.ModelChoiceField(
        queryset=SpecialInclusion.objects.filter(
            inclusion_type='general',
            status=True,
            is_available=True
        ),
        required=True,
        empty_label="Select Activity/Service",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'updateStandaloneInclusionPrice()'
        }),
        label="Activity/Service"
    )
    
    booking_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Booking Date"
    )
    
    booking_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        label="Booking Time (Optional)"
    )
    
    num_adults = forms.IntegerField(
        required=True,
        min_value=0,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'onchange': 'updateStandaloneInclusionPrice()'
        }),
        label="Number of Adults"
    )
    
    num_children = forms.IntegerField(
        required=True,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'onchange': 'updateStandaloneInclusionPrice()'
        }),
        label="Number of Children"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special instructions or notes...'
        }),
        label="Notes (Optional)"
    )
    
    class Meta:
        model = StandaloneInclusionBooking
        fields = [
            'special_inclusion',
            'booking_date',
            'booking_time',
            'num_adults',
            'num_children',
            'notes'
        ]
    
    def __init__(self, *args, **kwargs):
        """Initialize form with destination filter if provided"""
        destination = kwargs.pop('destination', None)
        super().__init__(*args, **kwargs)
        
        # Filter by destination if provided
        if destination:
            self.fields['special_inclusion'].queryset = SpecialInclusion.objects.filter(
                inclusion_type='general',
                status=True,
                is_available=True
            ).filter(
                models.Q(destination=destination) | models.Q(destination__isnull=True)
            )
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        num_adults = cleaned_data.get('num_adults', 0)
        num_children = cleaned_data.get('num_children', 0)
        
        # At least one participant required
        if num_adults == 0 and num_children == 0:
            raise forms.ValidationError(
                "At least one adult or child participant is required."
            )
        
        return cleaned_data


# your_app/forms.py
from django import forms
from .models import VehiclePricing

class VehiclePricingForm(forms.ModelForm):
    class Meta:
        model = VehiclePricing
        
        # ✅ FIXED: Changed 'pricing_type' back to 'type' to match your model
        fields = ['from_date', 'to_date', 'type', 'total_fee_100km', 'extra_fee_per_km', 'is_active']
        
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'total_fee_100km': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_fee_per_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        

class DayItineraryForm(forms.ModelForm):
    class Meta:
        model = DayItinerary
        fields = ['destination', 'name', 'details', 'created_by']
        

class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields = ['source_name', 'is_active']
        widgets = {
            'source_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter source name'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        

class PackageThemeForm(forms.ModelForm):
    class Meta:
        model = PackageTheme
        # created_by and created_at are set automatically
        fields = ['package_name', 'image', 'status']
        widgets = {
            'package_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['currency_name', 'currency_rate', 'status']
        widgets = {
            'currency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

class OrganisationalSettingForm(forms.ModelForm):
    class Meta:
        model = OrganisationalSetting
        fields = [
            'organization_name', 
            'email', 
            'phone_number', 
            'address', 
            'gstn', 
            'state', 
            'state_code'
        ]
        
        
from ckeditor.widgets import CKEditorWidget

# class InvoiceLogoForm(forms.ModelForm):
    

#     class Meta:
#         model = InvoiceLogo
#         fields = ['image']

# class InvoiceTermsForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())

#     class Meta:
#         model = InvoiceTerms
#         fields = ['content']

# class PackageTermsForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())

#     class Meta:
#         model = PackageTerms
#         fields = ['content']

# class BankInformationForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())

#     class Meta:
#         model = BankInformation
#         fields = ['content']


from ckeditor.widgets import CKEditorWidget
from .models import InvoiceLogo, InvoiceTerms, PackageTerms, BankInformation

class CombinedBusinessSettingsForm(forms.Form):
    image = forms.ImageField(required=False, label="Invoice Logo")

    invoice_terms = forms.CharField(
        widget=CKEditorWidget(),
        label="Invoice Terms & Conditions"
    )
    package_terms = forms.CharField(
        widget=CKEditorWidget(),
        required=False,
        label="Package Terms & Conditions"
    )
    bank_info = forms.CharField(
        widget=CKEditorWidget(),
        label="Bank Information"
    )

    def __init__(self, *args, **kwargs):
        invoice_logo = kwargs.pop('invoice_logo', None)
        invoice_terms = kwargs.pop('invoice_terms', None)
        package_terms = kwargs.pop('package_terms', None)
        bank_info = kwargs.pop('bank_info', None)
        super().__init__(*args, **kwargs)

        if invoice_logo:
            self.fields['image'].initial = invoice_logo.image
        if invoice_terms:
            self.fields['invoice_terms'].initial = invoice_terms.content
        if package_terms:
            self.fields['package_terms'].initial = package_terms.content
        if bank_info:
            self.fields['bank_info'].initial = bank_info.content

    def save(self, invoice_logo, invoice_terms, package_terms, bank_info):
        # Save logo
        if self.cleaned_data.get('image'):
            invoice_logo.image = self.cleaned_data['image']
            invoice_logo.save()

        # Save text content
        invoice_terms.content = self.cleaned_data['invoice_terms']
        invoice_terms.save()

        package_terms.content = self.cleaned_data['package_terms']
        package_terms.save()

        bank_info.content = self.cleaned_data['bank_info']
        bank_info.save()

        
        
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import PackageTermss

class PackageTermssForm(forms.ModelForm):
    class Meta:
        model = PackageTermss
        fields = [
            'special_inclusion',
            'package_inclusion',
            'package_exclusion',
            'terms_and_conditions',
            'payment_policy',
            'cancellation_policy',
            'refund_policy',
            'list_of_documents',
            'is_active'
        ]
        widgets = {
            'special_inclusion': CKEditorWidget(),
            'package_inclusion': CKEditorWidget(),
            'package_exclusion': CKEditorWidget(),
            'terms_and_conditions': CKEditorWidget(),
            'payment_policy': CKEditorWidget(),
            'cancellation_policy': CKEditorWidget(),
            'refund_policy': CKEditorWidget(),
            'list_of_documents': CKEditorWidget(),
        }

        

class BranchSettingsForm(forms.ModelForm):
    class Meta:
        model = BranchSettings
        fields = ['branch_name', 'location', 'status']
        
        
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['brand_name', 'parent_selection', 'role_name', 'status']
        widgets = {
            'brand_name': forms.Select(attrs={'class': 'form-control'}),
            'parent_selection': forms.Select(attrs={'class': 'form-control'}),
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
# Travel/forms.py

from django import forms
from Travel.models import Query, TeamMember

# Travel/forms.py

from django import forms
from .models import Query, TeamMember, LeadSource

class QueryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # ✅ Extract custom parameters
        self.user = kwargs.pop('user', None)
        self.user_role = kwargs.pop('user_role', None)
        
        super(QueryForm, self).__init__(*args, **kwargs)
        
        # ✅ HIDE assign field for regular users (non-admin/non-manager)
        if self.user_role not in ['superuser', 'admin', 'manager']:
            if 'assign' in self.fields:
                self.fields.pop('assign')
        
        # ✅ OPTIONAL: Make assign field show current user by default for admins
        if self.user_role in ['admin', 'manager'] and not self.instance.pk:
            # On create, pre-select current user in assign dropdown
            if 'assign' in self.fields and self.user:
                self.fields['assign'].initial = self.user
    
    class Meta:
        model = Query
        exclude = ['created_by', 'created_at']  # ✅ Auto-managed fields
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'remark': forms.Textarea(attrs={'rows': 3}),
        }



class ItineraryDayPlanForm(forms.ModelForm):
    class Meta:
        model = ItineraryDayPlan
        fields = ['itinerary', 'day_number', 'destination', 'notes', 'hotels', 'houseboats', 'activities', 'meal_plans', 'vehicles', 'inclusions']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'hotels': forms.CheckboxSelectMultiple,
            'activities': forms.CheckboxSelectMultiple,
            'meal_plans': forms.CheckboxSelectMultiple,
            'vehicles': forms.CheckboxSelectMultiple,
            'inclusions': forms.CheckboxSelectMultiple,
        }
        
        
class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = [
            'destination',
            'category',
            'room_type',
            'meal_plan',
            'option',
            'num_double_beds',
            'child_with_bed',
            'child_without_bed',
            'extra_beds',
            'check_in_date',
            'check_in_time',
            'check_out_date',
            'check_out_time',
        ]
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'meal_plan': forms.Select(attrs={'class': 'form-select'}),
            'option': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'num_double_beds': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}),
            'child_with_bed': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}),
            'child_without_bed': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}),
            'extra_beds': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': '0'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
        }
        
        labels = {
            'destination': 'Destination *',
            'category': 'Hotel Category *',
            'room_type': 'Room Type',
            'meal_plan': 'Meal Plan',
            'option': 'Booking Option *',
            'num_double_beds': 'Double Beds',
            'child_with_bed': 'Children with Bed',
            'child_without_bed': 'Children without Bed',
            'extra_beds': 'Extra Beds',
            'check_in_date': 'Check-in Date *',
            'check_in_time': 'Check-in Time *',
            'check_out_date': 'Check-out Date *',
            'check_out_time': 'Check-out Time *',
        }
        
        help_texts = {
            'num_double_beds': 'Number of rooms with double beds (rooms will match this)',
            'child_with_bed': 'Children requiring their own bed',
            'child_without_bed': 'Children sharing parent\'s bed',
        }
    
    def __init__(self, *args, package=None, **kwargs):
        """
        Accept package parameter for validation.
        Store package as instance variable for use in clean() method.
        """
        super().__init__(*args, **kwargs)
        
        self.package = package
        
        # Make certain fields not required
        self.fields['room_type'].required = False
        self.fields['meal_plan'].required = False
        
        # Set default values
        self.fields['num_double_beds'].initial = 0
        self.fields['child_with_bed'].initial = 0
        self.fields['child_without_bed'].initial = 0
        self.fields['extra_beds'].initial = 0
    
    def clean(self):
        """
        Custom validation for the hotel booking form.
        """
        cleaned_data = super().clean()
        
        # Get cleaned data
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        num_double_beds = cleaned_data.get('num_double_beds', 0)
        child_with_bed = cleaned_data.get('child_with_bed', 0)
        child_without_bed = cleaned_data.get('child_without_bed', 0)
        extra_beds = cleaned_data.get('extra_beds', 0)
        
        # ==========================================
        # ✅ DATE VALIDATION
        # ==========================================
        if check_in_date and check_out_date:
            if check_out_date <= check_in_date:
                raise forms.ValidationError(
                    'Check-out date must be after check-in date.'
                )
        
        # ==========================================
        # ✅ ROOM CONFIGURATION VALIDATION
        # ==========================================
        
        if num_double_beds is not None and num_double_beds < 0:
            raise forms.ValidationError('Number of double beds cannot be negative.')
        
        if child_with_bed is not None and child_with_bed < 0:
            raise forms.ValidationError('Children with bed count cannot be negative.')
        
        if child_without_bed is not None and child_without_bed < 0:
            raise forms.ValidationError('Children without bed count cannot be negative.')
        
        if extra_beds is not None and extra_beds < 0:
            raise forms.ValidationError('Extra beds count cannot be negative.')
        
        # ✅ Validate that at least some accommodation is specified
        total_accommodation = num_double_beds + extra_beds
        if total_accommodation == 0:
            self.add_error(
                'num_double_beds',
                forms.ValidationError(
                    'Please specify at least one double bed or extra bed.',
                    code='no_accommodation'
                )
            )
        
        return cleaned_data
    
    def clean_category(self):
        """Ensure category is provided"""
        category = self.cleaned_data.get('category')
        if not category or category.strip() == '':
            raise forms.ValidationError('Hotel category is required.')
        return category


# ==========================================
# NEW: Inline Form for Multiple Inclusions
# ==========================================
class HotelBookingInclusionForm(forms.Form):
    """
    Simple form for adding a single inclusion item.
    Use this in a formset or dynamically in the frontend.
    """
    special_inclusion_id = forms.IntegerField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Special Inclusion'
    )
    num_adults = forms.IntegerField(
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        label='Adults'
    )
    num_children = forms.IntegerField(
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        label='Children'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        num_adults = cleaned_data.get('num_adults', 0)
        num_children = cleaned_data.get('num_children', 0)
        
        if num_adults == 0 and num_children == 0:
            raise forms.ValidationError(
                'Please specify at least one adult or child for this inclusion.'
            )
        
        return cleaned_data


        
class ActivityBookingForm(forms.ModelForm):
    class Meta:
        model = ActivityBooking
        fields = [
            'booking_date', 
            'booking_time', 
            'num_adults', 
            'num_children', 
            'notes'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'num_adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }



from .models import VehicleBooking

class VehicleBookingForm(forms.ModelForm):
    class Meta:
        model = VehicleBooking
        fields = [
            'pickup_date', 
            'pickup_time', 
            'num_passengers', 
            'vehicle_type', 
            'option',
            'total_km',
        ]
        labels = {
            'pickup_date': 'Pickup Date*',
            'pickup_time': 'Pickup Time*',
            'num_passengers': 'Number of Passengers*',
            'vehicle_type': 'Vehicle Type*',
            'option': 'Options/Requirements*',
            'total_km': 'Total Kilometers',
        }
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'num_passengers': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., SUV, Sedan'}),
            'option': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AC/Non-AC'}),
            'total_km': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        

from .models import HouseboatBooking

class HouseboatBookingForm(forms.ModelForm):
    class Meta:
        model = HouseboatBooking
        fields = [
            'meal_plan', 'check_in_date', 'check_out_date', 'room_type',
            'num_one_bed_rooms', 'num_two_bed_rooms', 'num_three_bed_rooms',
            'num_four_bed_rooms', 'num_five_bed_rooms', 'num_six_bed_rooms',
            'num_seven_bed_rooms', 'num_eight_bed_rooms', 'num_nine_bed_rooms',
            'num_ten_bed_rooms', 'num_extra_beds'
        ]
        widgets = {
            'meal_plan': forms.Select(attrs={'class': 'form-select'}),
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'room_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ MOVED: The loop for number inputs is now correctly inside the __init__ method
        num_words = {
            1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 
            7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'
        }
        for i in range(1, 11):
            field_name = f'num_{num_words[i]}_bed_rooms'
            self.fields[field_name].widget.attrs.update({'class': 'form-control', 'min': '0'})
        
        self.fields['num_extra_beds'].widget.attrs.update({'class': 'form-control', 'min': '0'})