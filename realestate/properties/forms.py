from django import forms
from .models import Property, PropertyImage, Location

# Custom widget and field for multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
    
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)

# Main PropertyForm class
class PropertyForm(forms.ModelForm):
    district = forms.ChoiceField(
        choices=[],
        label="Select District"
    )
    area = forms.ChoiceField(
        choices=[],
        label="Select Area",
        required=True
    )
    
    images = MultipleFileField(label='Upload Images', required=False)
    
    class Meta:
        model = Property
        fields = ['title', 'description', 'property_type', 'type', 'price', 'bedrooms', 'bathrooms', 'area_sqft', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate district dropdown
        districts = Location.objects.values_list('district', flat=True).distinct()
        self.fields['district'].choices = [('', '----------')] + [(district, district) for district in districts]
        
        # Initialize empty area dropdown
        self.fields['area'].choices = [('', '----------')]
        
        # If form is being re-rendered with data, populate area dropdown
        if 'district' in self.data:
            try:
                district = self.data.get('district')
                areas = Location.objects.filter(district=district).values_list('area', flat=True).distinct()
                self.fields['area'].choices = [('', '----------')] + [(area, area) for area in areas]
            except (ValueError, TypeError):
                pass