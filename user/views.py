from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from user.models import User
from django.templatetags.static import static

# Create your views here.

def login_register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    login_form = LoginForm()
    register_form = RegisterForm()
    active_tab = 'login' 

    if request.method == 'POST':
        print(request.POST)
        if 'login_submit' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                try:
                    if '@' in username:
                        user_obj = User.objects.get(email=username)
                    else:
                        user_obj = User.objects.get(phone_number=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                    if user:
                        login(request, user)
                        return redirect('home')
                    else:
                        login_form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است')
                except User.DoesNotExist:
                    login_form.add_error(None, 'کاربری با این مشخصات یافت نشد')

        elif 'register_submit' in request.POST:
            register_form = RegisterForm(request.POST) 
            active_tab = 'register'
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.set_password(register_form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('home')
            else:
                print(register_form.errors) 

    context = {
        'form': login_form,
        'register': register_form,
        'acitve_tab': active_tab,
        'is_login': 'true' if active_tab == 'login' else 'false',

    }
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    form = ProfileForm(instance=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('profile')

    context = {
        'asus_laptop_url': static('assets/images/asus-laptop.webp'),
        'user' : user,
        'form' : form
    }
    return render(request, 'profile.html', context)