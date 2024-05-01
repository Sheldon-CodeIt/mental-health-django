from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def Home(request):
    return render (request,'baseApp/index.html')


def Test(request):
    return render (request,'baseApp/quiz.html')


def Demo(request):
    return render (request,'baseApp/test.html')