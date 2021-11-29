from django import forms
from django.contrib.auth.models import User

from . import models
from counts.models import Checking, Savings, Legal

class CheckingForm(forms.ModelForm):
    class Meta:
        model = Checking
        fields = '__all__'

class CheckingPersonForm(forms.ModelForm):
    class Meta:
        model = models.Checking_Person
        fields = '__all__'
        exclude = ('user', 'count',)

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = '__all__'


class SavingsPersonForm(forms.ModelForm):
    class Meta:
        model = models.Savings_Person
        fields = '__all__'
        exclude = ('user', 'count',)

class LegalForm(forms.ModelForm):
    class Meta:
        model = Legal
        fields = '__all__'

class JuridicalPersonForm(forms.ModelForm):
    class Meta:
        model = models.Legal_Person
        fields = '__all__'
        exclude = ('user', 'count',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
    )

    password_2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmation password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password_2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_data_2 = cleaned.get('password_2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_shot = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório!'


        #Usuários logados: Update
        if self.user:
            if user_data != user_db.username:
                if user_db:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_data != email_db.email:
                if email_db:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password_data_2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_2'] = error_msg_password_match
                    
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_shot

        #Usuários não logados: create
        else:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password_data_2:
                validation_error_msgs['password_2'] = error_msg_required_field

            if password_data:
                if password_data != password_data_2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_2'] = error_msg_password_match
                    
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_shot

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))

class UserJuridicalForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        label='Name'
    )

    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
    )

    password_2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmation password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password', 'password_2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password_data_2 = cleaned.get('password_2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_shot = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório!'


        #Usuários logados: Update
        if self.user:
            if user_data != user_db.username:
                if user_db:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_data != email_db.email:
                if email_db:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password_data_2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_2'] = error_msg_password_match
                    
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_shot

        #Usuários não logados: create
        else:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password_data_2:
                validation_error_msgs['password_2'] = error_msg_required_field

            if password_data:
                if password_data != password_data_2:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password_2'] = error_msg_password_match
                    
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_shot

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))