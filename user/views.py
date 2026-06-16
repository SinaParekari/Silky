from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileForm, AddressForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from user.models import User, Address, City, Province
from django.templatetags.static import static
from django.contrib import messages
from django.http import JsonResponse

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
def profile_view(request):

    user = request.user

    profile_form = ProfileForm(instance=user)
    address_form = AddressForm()

    # ALWAYS safe query
    addresses = Address.objects.filter(user=user)

    if request.method == "POST":

        # PROFILE UPDATE
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(
                request.POST,
                request.FILES,
                instance=user
            )

            if profile_form.is_valid():
                print("VALID")
                user_obj = profile_form.save(commit=False)

                password = profile_form.cleaned_data.get('password')
                if password:
                    user_obj.set_password(password)

                user_obj.save()
                print(user_obj.avatar)
                update_session_auth_hash(request, user_obj)

                return redirect('profile')

        # ADDRESS CREATE
        elif 'address_submit' in request.POST:

            # HARD LIMIT = 3 addresses
            if addresses.count() >= 3:
                messages.error(request, "حداکثر ۳ آدرس مجاز است.")
                return redirect('profile')

            address_form = AddressForm(request.POST)

            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()

                messages.success(request, "آدرس ثبت شد.")
                return redirect('profile')
        
        elif 'delete_address' in request.POST:
            address_id = request.POST.get('address_id')
            Address.objects.filter(id=address_id, user=request.user).delete()
            return redirect('profile')

    return render(request, 'profile.html', {
        'user': user,
        'form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
        'provinces': Province.objects.all(),

    })

def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)
