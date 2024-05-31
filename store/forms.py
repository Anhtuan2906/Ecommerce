from django import forms

from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].strip().title()

    def clean_description(self):
        return self.cleaned_data['description'].strip().capitalize()

    # def clean_category(self):
    #     categories = []
    #     for category in self.cleaned_data['categories']:
    #         if not Category.objects.filter(name=category).exists():
    #             raise forms.ValidationError(f"{category} is not a valid category")
    #         categories.append(Category.objects.get(name=category))
    #     self.cleaned_data['categories'] = categories
    #     return self.cleaned_data['categories']
