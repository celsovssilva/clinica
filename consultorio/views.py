from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'consultorio/home.html')


def servicos(request):
    return render(request, 'consultorio/servicos.html')