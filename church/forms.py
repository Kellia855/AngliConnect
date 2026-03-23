from django import forms
from .models import (
    Member,
    Role,
    MemberRole,
    Parish,
    Diocese,
    Baptism,
    Confirmation,
    Marriage,
    ServiceSession,
    AttendanceRecord,
)
import re


class MemberForm(forms.ModelForm):
    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.all(),
        required=True,
        empty_label="-- Select Diocese --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_diocese'})
    )
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'photo', 'diocese', 'parish']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-control', 'id': 'id_parish'}),
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Check if name contains only letters (no spaces, numbers, or symbols)
            if not re.match(r"^[a-zA-Z]+$", first_name):
                raise forms.ValidationError('First name can only contain letters.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Check if name contains only letters (no spaces, numbers, or symbols)
            if not re.match(r"^[a-zA-Z]+$", last_name):
                raise forms.ValidationError('Last name can only contain letters.')
        return last_name
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing member, set the diocese
        if self.instance and self.instance.pk and self.instance.parish:
            self.fields['diocese'].initial = self.instance.parish.diocese
        
        # Initially show all parishes or filter if diocese is selected
        if 'diocese' in self.data:
            try:
                diocese_id = int(self.data.get('diocese'))
                self.fields['parish'].queryset = Parish.objects.filter(diocese_id=diocese_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.parish:
            self.fields['parish'].queryset = Parish.objects.filter(diocese=self.instance.parish.diocese).order_by('name')
        else:
            self.fields['parish'].queryset = Parish.objects.none()
        
        self.fields['parish'].empty_label = "-- Select Parish --"


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MemberRoleForm(forms.ModelForm):
    class Meta:
        model = MemberRole
        fields = ['role', 'start_date', 'end_date']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BaptismForm(forms.ModelForm):
    class Meta:
        model = Baptism
        fields = [
            'member',
            'baptism_date',
            'parish',
            'church_name',
            'officiating_priest',
            'godparent1_name',
            'godparent1_gender',
            'godparent2_name',
            'godparent2_gender',
            'godparent3_name',
            'godparent3_gender',
            'notes',
        ]
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'baptism_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'officiating_priest': forms.TextInput(attrs={'class': 'form-control'}),
            'godparent1_name': forms.TextInput(attrs={'class': 'form-control'}),
            'godparent1_gender': forms.Select(attrs={'class': 'form-control'}),
            'godparent2_name': forms.TextInput(attrs={'class': 'form-control'}),
            'godparent2_gender': forms.Select(attrs={'class': 'form-control'}),
            'godparent3_name': forms.TextInput(attrs={'class': 'form-control'}),
            'godparent3_gender': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = Confirmation
        fields = [
            'member',
            'confirmation_date',
            'parish',
            'church_name',
            'confirming_bishop',
            'confirmation_verse',
            'notes',
        ]
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'confirming_bishop': forms.TextInput(attrs={'class': 'form-control'}),
            'confirmation_verse': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MarriageForm(forms.ModelForm):
    class Meta:
        model = Marriage
        fields = [
            'groom',
            'bride',
            'marriage_date',
            'parish',
            'church_name',
            'officiating_priest',
            'witness1_name',
            'witness2_name',
            'license_details',
            'notes',
        ]
        widgets = {
            'groom': forms.Select(attrs={'class': 'form-control'}),
            'bride': forms.Select(attrs={'class': 'form-control'}),
            'marriage_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'officiating_priest': forms.TextInput(attrs={'class': 'form-control'}),
            'witness1_name': forms.TextInput(attrs={'class': 'form-control'}),
            'witness2_name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_details': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ServiceSessionForm(forms.ModelForm):
    class Meta:
        model = ServiceSession
        fields = ['session_date', 'service_type', 'notes']
        widgets = {
            'session_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class AttendanceCheckInForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
