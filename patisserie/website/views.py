from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserProfileForm, ItemFilterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Item, UserProfile, Cart, CartItem
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

# Home view for the landing page
def home(request):
    return render(request, 'home.html')

# User registration view    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')  
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

# User profile view for displaying and updating user profile information
@login_required
def profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'profile_form': profile_form})

# Browse items view for displaying items with filtering options
def browse_items(request):
    items = Item.objects.all()

     # Apply item filtering based on the submitted form data
    item_filter_form = ItemFilterForm(request.GET)
    if item_filter_form.is_valid():
        name_filter = item_filter_form.cleaned_data.get('name')
        min_price_filter = item_filter_form.cleaned_data.get('min_price')
        max_price_filter = item_filter_form.cleaned_data.get('max_price')
        category_filter = item_filter_form.cleaned_data.get('category')
        sub_category_filter = item_filter_form.cleaned_data.get('sub_category')

        if name_filter:
            items = items.filter(name__icontains=name_filter)

        if min_price_filter:
            items = items.filter(price__gte=min_price_filter)

        if max_price_filter:
            items = items.filter(price__lte=max_price_filter)

        if category_filter:
            items = items.filter(category=category_filter)

        if sub_category_filter:
            items = items.filter(sub_category=sub_category_filter)
            
    return render(request, 'browse_items.html', {'items': items, 'item_filter_form': item_filter_form})

# Guest browse items view for displaying items to non-logged in users with filtering options    
def guest_browse_items(request):
    items = Item.objects.all()

    # Apply item filtering based on the submitted form data
    item_filter_form = ItemFilterForm(request.GET)
    if item_filter_form.is_valid():
        name_filter = item_filter_form.cleaned_data.get('name')
        min_price_filter = item_filter_form.cleaned_data.get('min_price')
        max_price_filter = item_filter_form.cleaned_data.get('max_price')
        category_filter = item_filter_form.cleaned_data.get('category')
        sub_category_filter = item_filter_form.cleaned_data.get('sub_category')

        if name_filter:
            items = items.filter(name__icontains=name_filter)

        if min_price_filter:
            items = items.filter(price__gte=min_price_filter)

        if max_price_filter:
            items = items.filter(price__lte=max_price_filter)

        if category_filter:
            items = items.filter(category=category_filter)

        if sub_category_filter:
            items = items.filter(sub_category=sub_category_filter)
            
    return render(request, 'guest_browse_items.html', {'items': items, 'item_filter_form': item_filter_form})

# Custom user_passes_test function to check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Add item view for admins to add new items to the E-shop
@login_required
@user_passes_test(is_admin)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('browse_items') 
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})

# Add item to cart view for logged-in users to add items to their cart    
@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)

   
    try:
        cart_item = user_cart.cartitem_set.get(item=item)
      
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        
        cart_item = CartItem.objects.create(cart=user_cart, item=item)

    return redirect('cart')

# View cart view for displaying the items in the user's cart
@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Remove all items from cart view for logged-in users to empty their cart
@login_required
def remove_all_from_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        return redirect('cart')
    
    return render(request, 'remove_all_from_cart.html') 
    
