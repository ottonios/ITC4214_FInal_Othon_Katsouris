from django.contrib import admin
from .models import Category, SubCategory, Item

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo',)
    # Customize other fields as needed

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'photo',)
    # Customize other fields as needed

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Item)