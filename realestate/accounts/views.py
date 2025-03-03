from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import UserRegistrationForm
from .models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Changed from login to auth_login
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):  # Changed function name from login to user_login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Changed from login to auth_login
            return redirect('user_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')


#dashboard view

User = get_user_model()  # Get your custom User model
@login_required
def user_dashboard(request):
 
    # Get user details
    user = request.user
    
    
    # Get user's properties or other relevant data
    # user_properties = Property.objects.filter(user=user)

    return render(request, 'accounts/user_dashboard.html', {'user': user})

#logout view

def logout_view(request):
    logout(request)
    return redirect('login')