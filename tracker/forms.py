from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Expense, Category, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(models.Q(user=user) | models.Q(is_predefined=True))

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(models.Q(user=user) | models.Q(is_predefined=True))
            # Nullable category for overall budget
            self.fields['category'].required = False
            self.fields['category'].empty_label = "Overall (No Specific Category)"
