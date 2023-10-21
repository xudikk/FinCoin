from django import forms
from core.models import Product, New, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
