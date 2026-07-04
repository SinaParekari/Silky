from django.shortcuts import render

# Create your views here.

def weblog(request):
    return render(request,'weblog.html')

def single_post(request):
    return render(request,'post.html')
