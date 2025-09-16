from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Paciente, Horario, Agendamento
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request,'consultorio/home.html')

def servicos(request):
    return render(request, 'consultorio/servicos.html')

@login_required
def principalMedico(request):
    medico = Medico.objects.get(user=request.user)
    agora = datetime.now()
    hoje = agora.date()
    
   
    pacientesDoDia = Agendamento.objects.filter(
        medico=medico,
        horario__dia__gte=hoje,
        horario__hora__gte=agora.time()
    ).order_by('horario__hora')

    
    horariosDisponiveis = Horario.objects.filter(
        medico=medico,
        dia__gte=hoje
    ).order_by('dia', 'hora')
    
   
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
    paciente = Paciente.objects.get(user=request.user)
    medicos = Medico.objects.all()
    agora = datetime.now()

    agendamentos = Agendamento.objects.filter(
        paciente=paciente,
        status='pendente',
        horario__dia__gte=agora.date(),
    ).order_by('horario__dia', 'horario__hora')

    for medico in medicos:
        medico.horarios_disponiveis = Horario.objects.filter(
            medico=medico,
            disponibilidade=True
        ).filter(
            Q(dia__gt=agora.date()) | Q(dia=agora.date(), hora__gte=agora.time())
        ).order_by('dia', 'hora')

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "agendar":
            medico_id = request.POST.get("medico_id")
            horario_id = request.POST.get("horario_id")
            horario = Horario.objects.get(id=horario_id)
            medico = Medico.objects.get(id=medico_id)

            if horario.disponibilidade:
                Agendamento.objects.create(paciente=paciente, medico=medico, horario=horario)
                horario.disponibilidade = False
                horario.save()
                messages.success(request, "Consulta agendada com sucesso")
            else:
                messages.error(request, "Esse horário está indisponível")
            return redirect("principal")

        elif acao == "cancelar":
            agendamento_id = request.POST.get("agendamento_id")
            agendamento = Agendamento.objects.get(id=agendamento_id, paciente=paciente)
            agendamento.status = "cancelado"
            agendamento.save()
            agendamento.horario.disponibilidade = True
            agendamento.horario.save()
            messages.success(request, "Consulta cancelada com sucesso")
            return redirect("principal")

        elif acao == "remarcar":
            agendamento_id = request.POST.get("agendamento_id")
            novo_horario_id = request.POST.get("novo_horario_id")

            try:
                agendamento = Agendamento.objects.get(id=agendamento_id, paciente=paciente)
                novo_horario = Horario.objects.get(id=novo_horario_id)

                if not novo_horario.disponibilidade:
                    messages.error(request, "Novo horário indisponível")
                else:
                    horario_antigo = agendamento.horario
                    horario_antigo.disponibilidade = True
                    horario_antigo.save()
                
                    agendamento.horario = novo_horario
                    agendamento.status = 'pendente'
                    agendamento.save()

                    novo_horario.disponibilidade = False
                    novo_horario.save()

                    messages.success(request, "Consulta remarcada com sucesso")
            
            except Agendamento.DoesNotExist:
                messages.error(request, "Agendamento não encontrado")
            except Horario.DoesNotExist:
                messages.error(request, "Horário não encontrado")
            
            return redirect("principal")

    context = {
        'medicos': medicos,
        'agendamentos': agendamentos
    }
    return render(request, 'consultorio/principal.html', context)

def concluido(request,agendamento_id):
    agendamento= get_object_or_404(Agendamento,id=agendamento_id,medico__user=request.user)

    agendamento.status="concluido"
    agendamento.concluido= True
    agendamento.save()
    agendamento.horario.disponibilidade=False
    agendamento.horario.save()
    return redirect('principalMedico')