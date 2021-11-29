from django.db import models
from django.contrib.auth.models import User

class Count(models.Model):
    agency = models.CharField('Agency', max_length=6)
    count = models.CharField('Count', max_length=7)
    balance = models.DecimalField('Balance', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.agency

    class Meta:
        abstract = True

class Checking(Count):
    limit = models.DecimalField('Limit', max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = 'Checking'
        verbose_name_plural = 'Checkings'

class Savings(Count):
    
    class Meta:
        verbose_name = 'Saving'
        verbose_name_plural = 'Savings'

class Legal(Count):
    limit = models.DecimalField('Limit', max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = 'Juridical'
        verbose_name_plural = 'Juridicals'