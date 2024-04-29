from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def Home(request):
    return render (request,'baseApp/index.html')