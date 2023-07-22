from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserProfileForm, ItemFilterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Item, UserProfile, Cart, CartItem
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')  # Redirect to the user's profile page after successful registration
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

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

def browse_items(request):
    items = Item.objects.all()

    # Handle filters for name, price, category, and subcategory
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
    
def guest_browse_items(request):
    items = Item.objects.all()

    # Handle filters for name and price
    name_filter = request.GET.get('name')
    min_price_filter = request.GET.get('min_price')
    max_price_filter = request.GET.get('max_price')

    if name_filter:
        items = items.filter(name__icontains=name_filter)

    if min_price_filter:
        items = items.filter(price__gte=min_price_filter)

    if max_price_filter:
        items = items.filter(price__lte=max_price_filter)

    item_filter_form = ItemFilterForm(request.GET)
    

    return render(request, 'guest_browse_items.html', {'items': items, 'item_filter_form': item_filter_form})

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('browse_items')  # Redirect to the browsing page after adding the item
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})
    
@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart for the user
    try:
        cart_item = user_cart.cartitem_set.get(item=item)
        # Increment the quantity if the item is already in the cart
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # Add the item to the cart with a quantity of 1 if it's not already in the cart
        cart_item = CartItem.objects.create(cart=user_cart, item=item)

    return redirect('cart')

@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_all_from_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        return redirect('cart')
    
    return render(request, 'remove_all_from_cart.html')  # Create a template for this page if needed
    