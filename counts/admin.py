from django.contrib import admin
from . import models

@admin.register(models.Checking)
class CheckingCount(admin.ModelAdmin):
    list_display = ('count', 'agency', 'balance')

@admin.register(models.Savings)
class SavingsCount(admin.ModelAdmin):
    list_display = ('count', 'agency', 'balance')

@admin.register(models.Legal)
class JuridicalCount(admin.ModelAdmin):
    list_display = ('count', 'agency', 'balance')