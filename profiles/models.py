from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from utils.validacpf import valida_cpf

class Person(models.Model):
    BANK_NAMES = (
        ('NB', 'Não é um banco'),
        ('BB', 'Banco do Basil'),
        ('IT', 'Itaú'),
        ('CX', 'Caixa'),
        ('BD', 'Bradesco'),
        ('ST', 'Santander'),
        ('C6', 'C6 Bank'),
        ('BP', 'BTG Pactual'),
        ('NU', 'Nubank'),
        ('IN', 'Inter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    date = models.DateField('Date create/Bday', )
    bank = models.CharField(
        max_length=14,
        default='NB',
        choices=BANK_NAMES
    )

    def clean(self):
        error_messages = {}

        if self.bank == 'NAB':
            error_messages['bank'] = 'Selecione um banco por favor!'

    class Meta:
        abstract = True

class Checking_Person(Person):
    cpf = models.CharField('CPF', max_length=11)
    count = models.OneToOneField('counts.Checking', on_delete=models.CASCADE, verbose_name='Checking count') 

    def clean(self):
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Por favor digite um cpf válido!'

        if error_messages:
            raise ValidationError(error_messages)         
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Checking'
        verbose_name_plural = 'Checking_people'

class Savings_Person(Person):
    cpf = models.CharField('CPF', max_length=11)
    count = models.OneToOneField('counts.Savings', on_delete=models.CASCADE, verbose_name='Saving count')

    def clean(self):
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Por favor digite um cpf válido'

        if error_messages:
            raise ValidationError(error_messages)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'        
        
    class Meta:
        verbose_name = 'Saving'
        verbose_name_plural = 'Savings'

class Legal_Person(Person):
    cnpj = models.CharField('CNPJ', max_length=18)
    indentification = models.CharField('Indentification', max_length=14)
    count = models.OneToOneField('counts.Legal', on_delete=models.CASCADE, verbose_name='Juridical count')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Juridical'
        verbose_name_plural = 'Juridicals'