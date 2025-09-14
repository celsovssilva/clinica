# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PacienteSignUpForm, MedicoSignUpForm, PacienteLogin, MedicoLoginForm


def paciente(request):
    if request.method == 'POST':
        form = PacienteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('paciente_login')
    else:
        form = PacienteSignUpForm()
    return render(request, 'registration/paciente.html', {'form': form})

def medico(request):
    if request.method == 'POST':
        form = MedicoSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('medico_login')
    else:
        form = MedicoSignUpForm()
    return render(request, 'registration/medico.html', {'form': form})

def pacienteLogin(request):
    if request.method == 'POST':
        form = PacienteLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('principal')
    else:
        form = PacienteLogin()
    return render(request, 'registration/pacienteLogin.html', {'form': form})

def medicoLogin(request):
    if request.method == 'POST':
        form = MedicoLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('principalMedico')
    else:
        form = MedicoLoginForm()
    return render(request, 'registration/medicoLogin.html', {'form': form})


