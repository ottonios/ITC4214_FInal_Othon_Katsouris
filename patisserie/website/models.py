from django.contrib.auth.models import User
from django.db import models

# User Profile model for extending the built-in User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-One relationship with the User model
    bio = models.TextField(blank=True)# Optional user bio
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True) # User profile picture

    def __str__(self):
        return self.user.username # Return the username as the string representation of the UserProfile instance

# Category model for item categorization        
class Category(models.Model):
    name = models.CharField(max_length=100) # Name of the category
    photo = models.ImageField(upload_to='category_photos/', blank=True, null=True)  # Category photo (optional)

    def __str__(self):
        return self.name # Return the category name as the string representation of the Category instance

# SubCategory model for further item categorization under a main category
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # ForeignKey relationship with the Category model
    name = models.CharField(max_length=100)  # Name of the subcategory
    photo = models.ImageField(upload_to='subcategory_photos/', blank=True, null=True) # Subcategory photo (optional)

    def __str__(self):
        return f"{self.category} - {self.name}" # Return the subcategory name with its parent category as the string representation of the SubCategory instance

# Item model for representing individual items in the E-shop
class Item(models.Model):
    name = models.CharField(max_length=100) # Name of the item
    description = models.TextField() # Description of the item
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price of the item
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # ForeignKey relationship with the Category model
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE) # ForeignKey relationship with the SubCategory model
    image = models.ImageField(upload_to='item_images/')   # Image of the item

    def __str__(self):
        return self.name  # Return the item name as the string representation of the Item instance
    
      # Cart model for representing user's cart containing multiple items  
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey relationship with the User model
    items = models.ManyToManyField(Item, through='CartItem')  # ManyToMany relationship with the Item model via CartItem
    quantity = models.PositiveIntegerField(default=1)  # Quantity of items in the cart
    date_added = models.DateTimeField(auto_now_add=True) # Date and time when the cart was created

# CartItem model for representing the items in the user's cart with quantity and date added    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # ForeignKey relationship with the Cart model
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # ForeignKey relationship with the Item model
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the item in the cart
    date_added = models.DateTimeField(auto_now_add=True) # Date and time when the item was added to the cart

# Profile model for extending the built-in User model with an additional profile picture    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-One relationship with the User model  
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # User profile picture (optional)
