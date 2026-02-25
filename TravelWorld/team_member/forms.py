# team_member/forms.py

from django import forms
from Travel.models import TeamMember


class TeamMemberForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=False,
        help_text='Leave blank to keep current password'
    )
    
    class Meta:
        model = TeamMember
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters')
        return password
