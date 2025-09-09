from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import PacienteSignUpForm, MedicoSignUpForm
from .models import Paciente,Medico

# Create your views here.

def paciente(request):
    if request.method== 'POST':
        form = PacienteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Paciente.objects.create(
                user=user,
                cpf=form.cleaned_data.get('cpf'),
                data_nascimento= form.cleaned_data.get('data_nascimento'),
                telefone=form.cleaned_data.get('telefone')
            )
            login(request,user)
            return redirect("principal")
    else:
        form= PacienteSignUpForm()
    return render(request,'registration/paciente.html', {'form': form})


def medico(request):
    if request.method == 'POST':
        form = MedicoSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            Medico.objects.create(
                user=user,
                especialidade=form.cleaned_data.get('especialidade')
            )
            login(request,user)
            return redirect('principalmedico')
    else:
        form= MedicoSignUpForm()
    return render(request, 'registration/medico.html', {'form':form})
