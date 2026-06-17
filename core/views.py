from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from cart.models import Cart

# Create your views here.

def home_page(request):
    return render(request, 'home_page.html')

def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('contact')

    context = {
        'form': form,
    }
    return render(request, 'contact-us.html', context)


def cart_context(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None

    return {
        'cart': cart
    }

