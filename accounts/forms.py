# clinicahn/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm


class PacienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telefone = forms.CharField(max_length=15)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class MedicoSignUpForm(UserCreationForm):
    crm = forms.CharField(max_length=20)
    especialidade = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')