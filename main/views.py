from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignInForm, SignUpForm, ProductForm, BuyerSignUpForm, SellerSignUpForm
from .models import Cart, CartItem, Product, CustomUser
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from .decorators import buyer_required, seller_required

def role_selection(request):
    return render(request, 'role_selection.html')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("User authenticated and logged in")  # Debugging statement
                return redirect('index')  # Redirect to the home page after successful login
            else:
                print("Invalid email or password")  # Debugging statement
                messages.error(request, 'Invalid email or password.')
        else:
            print("Sign-in form is not valid")  # Debugging statement
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(f"User created: {user.username}, {user.role}, {user.id}")  # Debugging statement
            # Authenticate the user
            user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                print("User signed up and logged in")  # Debugging statement
                return redirect('index')  # Redirect to the home page
            else:
                print("Authentication failed")  # Debugging statement
        else:
            print("Signup form is not valid")  # Debugging statement
            print(form.errors)  # Print form errors for debugging
    else:
        form = BuyerSignUpForm()
    return render(request, 'buyer_signup.html', {'form': form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'seller'
            user.save()
            print(f"User created: {user.username}, {user.role}, {user.id}")  # Debugging statement
            # Authenticate the user
            user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                print("User signed up and logged in")  # Debugging statement
                return redirect('index')  # Redirect to the home page
            else:
                print("Authentication failed")  # Debugging statement
        else:
            print("Signup form is not valid")  # Debugging statement
            print(form.errors)  # Print form errors for debugging
    else:
        form = SellerSignUpForm()
    return render(request, 'seller_signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    return render(request, 'index.html', {'genres': genres, 'user': request.user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Get the backend
            backend = get_backends()[0]
            login(request, user, backend=backend)
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@buyer_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'cart_detail.html', context)

@login_required
@seller_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
@buyer_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    print(f"Cart: {cart}, Created: {created}")  # Debugging statement
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    print(f"CartItem: {cart_item}, Created: {created}")  # Debugging statement
    if not created:
        cart_item.add_quantity()
    else:
        cart_item.save()
    messages.success(request, 'Product added to cart!')
    return redirect('cart_detail')

@login_required
@buyer_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.remove_quantity()
    messages.success(request, 'Product removed from cart!')
    return redirect('cart_detail')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Example logic for recommended products
    recommended_products = Product.objects.filter(genre=product.genre).exclude(id=product.id)[:5]

    return render(request, 'product_detail.html', {
        'product': product,
        'recommended_products': recommended_products,
    })

def genre_products(request, genre):
    products = Product.objects.filter(genre=genre)
    return render(request, 'genre_products.html', {'products': products, 'genre': genre})

@login_required
@seller_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product removed successfully!')
    return redirect('genre_products', genre=product.genre)

def get_to_know_us(request):
    return render(request, 'get_to_know_us.html')

def payment_success(request):
    return render(request, 'success.html')

@login_required
def payment_cancel(request):
    return render(request, 'cancel.html')

def search(request):
    query = request.GET.get('q')
    print(f"Search query: {query}")  # Debugging line
    if query:
        products = Product.objects.filter(name__icontains=(query))
    else:
        products = Product.objects.all()
    return render(request, 'search_results.html', {'products': products, 'query': query})