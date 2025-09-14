from django.db import models

from accounts.models import Medico, Paciente


# Create your models here.


class Horario(models.Model):
    medico =models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia= models.DateField()
    hora = models.TimeField()
    disponibilidade= models.BooleanField(default=True)


    class Meta:
        unique_together=("medico","dia","hora")

    def __str__(self):
        return f"{self.dia} ás {self.hora} - {self.medico}"
    


class Agendamento(models.Model):
    paciente= models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico= models.ForeignKey(Medico,on_delete=models.CASCADE)
    horario = models.OneToOneField(Horario,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paciente} com {self.medico} às {self.horario}"