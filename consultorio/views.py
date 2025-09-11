from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'consultorio/home.html')


def servicos(request):
    return render(request, 'consultorio/servicos.html')
@login_required
def principalMedico(request):
    return render(request, 'consultorio/principalmedico.html')

@login_required
def principal(request):
    return render(request, 'consultorio/principal.html')