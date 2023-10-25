from django import forms
from core.models import Product, New, Category, Algorithm


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


class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = Algorithm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        root = kwargs.pop('creator')
        super().__init__(*args, **kwargs)
        self.fields['creator'].initial = root
