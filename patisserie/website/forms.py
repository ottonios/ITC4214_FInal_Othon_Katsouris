from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Category, SubCategory, Item

# Form for user registration
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
# Form for updating user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        
# Form for filtering items based on various criteria        
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
                # Filter sub-categories based on the selected category
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.is_bound:
            # If form is bound but no category is selected, display no sub-categories
            self.fields['sub_category'].queryset = SubCategory.objects.none()
            
# Form for adding or updating an item 
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category', 'sub_category', 'image']
