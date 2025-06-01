from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'license_plate', 'color', 'mileage', 'rental_cost_per_day', 'is_available', 'image']
