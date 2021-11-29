from django.contrib import admin
from .models import Checking_Person, Savings_Person, Legal_Person

@admin.register(Checking_Person)
class Checking(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'count')
    list_filter = ('bank',)

@admin.register(Savings_Person)
class Savings(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'count')
    list_filter = ('bank',)

@admin.register(Legal_Person)
class Juridical(admin.ModelAdmin):
    list_display = ('user', 'cnpj', 'indentification', 'count')
    list_filter = ('bank',)
