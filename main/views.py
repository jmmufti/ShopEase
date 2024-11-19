from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignInForm, SignUpForm, ProductForm
from .models import Cart, CartItem, Product

def index(request):
    genres = [
        ('clothing', 'Clothing'),
        ('personal_accessories', 'Personal Accessories'),
        ('ornamentation', 'Ornamentation'),
        ('gadgets', 'Gadgets'),
        ('beauty_personal_care', 'Beauty & Personal Care'),
        ('pet_accessories', 'Pet Accessories'),
        ('tour_trips', 'Tour & Trips'),
        ('women_clothing', 'Women Clothing'),
    ]
    return render(request, 'index.html', {'genres': genres})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Sign in successful!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            backend = 'shopease.auth_backends.EmailAuthBackend'
            user.backend = backend
            login(request, user, backend=backend)
            messages.success(request, 'Sign up successful!')
            return redirect('index')
        else:
            messages.warning(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'cart_detail.html', {'cart_items': cart_items})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            print(f"Product added: {product.name}, Genre: {product.genre}")
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.add_quantity()
    return redirect('cart_detail')  # Redirect to cart page

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.remove_quantity()
    return redirect('cart_detail')  # Redirect to cart page

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def genre_products(request, genre):
    products = Product.objects.filter(genre=genre)
    return render(request, 'genre_products.html', {'products': products, 'genre': genre})

def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('genre_products', genre=product.genre)