# clinicahn/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from accounts.models import Paciente, Medico, Especialidade

class PacienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telefone = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'cpf', 'data_nascimento', 'telefone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

    def clean_cpf(self):
        cpf = re.sub(r'[^0-9]', '', self.cleaned_data.get('cpf'))
        if len(cpf) != 11:
            raise ValidationError("CPF deve ter 11 dígitos.")
        return cpf

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Paciente.objects.create(
                user=user,
                cpf=self.cleaned_data['cpf'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                telefone=self.cleaned_data['telefone']
            )
        return user

class MedicoSignUpForm(UserCreationForm):
    crm = forms.CharField(max_length=20)
    especialidade = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'crm', 'especialidade']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

    def clean_crm(self):
        crm = self.cleaned_data.get('crm')
        if not crm.isdigit():
            raise ValidationError("CRM deve conter apenas números.")
        return crm

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            especialidade_nome = self.cleaned_data['especialidade']
            especialidade_obj, _ = Especialidade.objects.get_or_create(nome=especialidade_nome)
            Medico.objects.create(
                user=user,
                crm=self.cleaned_data['crm'],
                especialidade=especialidade_obj
            )
        return user


class PacienteLogin(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Email não encontrado.")
            if not user.check_password(password):
                raise forms.ValidationError("Senha inválida.")
            self.user_cache = user
        return self.cleaned_data


class MedicoLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Email ou senha inválidos.")
            try:
                user.medico
            except Medico.DoesNotExist:
                raise forms.ValidationError("Você não tem permissão para acessar esta área.")
            if not user.check_password(password):
                raise forms.ValidationError("Email ou senha inválidos.")
            self.user_cache = user
        return self.cleaned_data
