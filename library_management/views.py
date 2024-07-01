from django.shortcuts import render 

def home(request,brand_slug=None): 
    return render(request, 'home.html')