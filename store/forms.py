from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].strip().title()

    def clean_category(self):
        return self.cleaned_data['category'].strip().title()

    def clean_description(self):
        return self.cleaned_data['description'].strip().capitalize()
