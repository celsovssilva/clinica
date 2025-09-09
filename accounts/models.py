from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11,unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    


class Medico(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    crm = models.CharField(max_length=10, unique=True) 
    especialidade= models.CharField(max_length=100)

    def __str__(self):
        return self.user.username





