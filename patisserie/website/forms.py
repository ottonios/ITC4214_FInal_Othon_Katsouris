from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Category, SubCategory, Item

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        
class ItemFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.is_bound:
            self.fields['sub_category'].queryset = SubCategory.objects.none()
 
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category', 'sub_category', 'image']