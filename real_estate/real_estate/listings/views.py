from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ListingForm
from .models import Listing
from django.contrib.auth.decorators import login_required


# Головна сторінка
def home(request):
    listings = Listing.objects.all()
    return render(request, 'listings/home.html', {'listings': listings})

# Реєстрація
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'listings/register.html', {'form': form})

# Логін
def login_view(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('home') 
    else:
        form = AuthenticationForm()
    return render(request, 'listings/login.html', {'form': form})
@login_required
def profile(request):
    listings = Listing.objects.filter(user=request.user)
    return render(request, 'listings/profile.html', {'listings': listings})

# Додавання оголошення
@login_required(login_url='/login/')
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'listings/add_listing.html', {'form': form})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})


def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == "POST":
        listing.delete()
        return redirect('/')
    return render(request, 'listings/delete_listing.html', {'listing': listing})
