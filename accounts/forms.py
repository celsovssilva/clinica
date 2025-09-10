# clinicahn/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class PacienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telefone = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'cpf', 'data_nascimento', 'telefone',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z]+$', username):
            raise ValidationError("O nome de usuário deve conter apenas letras.")
        return username

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11:
            raise ValidationError("CPF deve ter 11 dígitos.")
        return cpf
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class MedicoSignUpForm(UserCreationForm):
    crm = forms.CharField(max_length=20)
    especialidade = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'crm', 'especialidade',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z]+$', username):
            raise ValidationError("O nome de usuário deve conter apenas letras.")
        return username
    
    def clean_crm(self):
        crm = self.cleaned_data.get('crm')
        if not crm.isdigit():
            raise ValidationError("CRM deve conter apenas números.")
        return crm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class PacienteLogin(AuthenticationForm):
    username = forms.EmailField(label="email",widget=forms.EmailInput(attrs={'autofocus': True, 'class':'form-control'}))

    def clean(self):
        email= self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if email and password:
            User = get_user_model()
            try:
                user= User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("email não encontrado", code= 'invalid_login')
            else:
                if not user.check_password(password):
                    raise forms.ValidationError("senha inválida", code="invalid_login")
                self.user_cache = user
        return self.cleaned_data
        


class MedicoLoginForm(AuthenticationForm):
    # O campo `username` deve ser renomeado para `email`
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            User = get_user_model()
            try:
                
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                
                raise forms.ValidationError("Email ou senha inválidos.", code='invalid_login')
            else:
                if not user.check_password(password):
                    raise forms.ValidationError("Email ou senha inválidos.", code='invalid_login')
               
                self.user_cache = user
        return self.cleaned_data