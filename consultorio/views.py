from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Paciente, Horario, Agendamento


# Create your views here.

def home(request):
    return render(request,'consultorio/home.html')


def servicos(request):
    return render(request, 'consultorio/servicos.html')


@login_required
def principalMedico(request):
    medico = Medico.objects.get(user=request.user)
    hoje = datetime.today().date()

    pacientesDoDia = Agendamento.objects.filter(medico=medico,horario__dia=hoje).order_by('horario__hora')

    horariosDisponiveis = Horario.objects.filter(medico=medico).order_by('dia', 'hora')

    if request.method == "POST":
        dia = request.POST.get("dia")
        hora = request.POST.get("hora")
        hora2 = datetime.strptime(hora, "%H:%M").time()

        if hora2.minute != 0:
            messages.error(request, "Só é permitido cadastrar em hora cheia.")
        elif Horario.objects.filter(medico=medico, dia=dia, hora=hora2, disponibilidade=True).exists():
            messages.error(request, "Esse horário já está indisponível.")
        else:
            Horario.objects.create(medico=medico, dia=dia, hora=hora2)
            messages.success(request, "Horário cadastrado com sucesso!")

        return redirect("principalMedico")

    return render(request, 'consultorio/principalmedico.html', {
        'pacientesDoDia': pacientesDoDia,
        'horariosDisponiveis': horariosDisponiveis
    })



@login_required
def principal(request):
    paciente= Paciente.objects.get(user=request.user)
    medicos = Medico.objects.all()
    
    if request.method == "POST":
        medico_id= request.POST.get("medico_id")
        horario_id= request.POST.get("horario_id")
        horario = Horario.objects.get(id=horario_id)
        medico = Medico.objects.get(id=medico_id)

        if horario.disponibilidade:
            Agendamento.objects.create(paciente=paciente,medico=medico, horario=horario)
            horario.disponibilidade= False
            horario.save()
            messages.success(request,"consulta agendada com sucesso")
        else:
            messages.error(request,"esse horario está indisponivel")
        return redirect('principal')
    context = {'medicos': medicos}
    return render(request, 'consultorio/principal.html', context)