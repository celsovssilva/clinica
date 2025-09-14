from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username



class Especialidade(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crm = models.CharField(max_length=10, unique=True, default='0')
    
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    

