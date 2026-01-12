from django import forms
from .models import Member, Role, MemberRole, Parish, Diocese


class MemberForm(forms.ModelForm):
    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.all(),
        required=True,
        empty_label="-- Select Diocese --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_diocese'})
    )
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone', 'diocese', 'parish']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-control', 'id': 'id_parish'}),
        }
    
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
