from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from profiles import models
from .models import Checking, Legal, Savings

class DepositView(View):
    template_name = 'counts/deposit.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        deposit = int(self.request.POST.get('deposit'))
        
        if not deposit:
            messages.error(
                self.request,
                'Digite um valor válido para o depósito.'
            )
            return redirect('counts:deposit')

        user = self.request.user
        
        checking = models.Checking_Person.objects.all().filter(user=user).first()
        saving = models.Savings_Person.objects.all().filter(user=user).first()
        juridical = models.Legal_Person.objects.all().filter(user=user).first()

        count = None

        if checking:
            count = Checking.objects.all().filter(agency=checking.count.agency).first()
            count.balance += deposit
            count.save()

        if saving:
            count = Savings.objects.all().filter(agency=saving.count.agency).first()
            count.balance += deposit
            count.save()
        
        if juridical:
            count = Legal.objects.all().filter(agency=juridical.count.agency).first()
            count.balance += deposit
            count.save()

        return redirect('counts:deposit')

class WithdrawView(View):
    template_name = 'counts/withdraw.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        withdraw = int(self.request.POST.get('withdraw'))
        
        if not withdraw:
            messages.error(
                self.request,
                'Digite um valor válido para o saque.'
            )
            return redirect('counts:withdraw')

        user = self.request.user
        
        checking = models.Checking_Person.objects.all().filter(user=user).first()
        saving = models.Savings_Person.objects.all().filter(user=user).first()
        juridical = models.Legal_Person.objects.all().filter(user=user).first()

        count = None

        if checking:
            count = Checking.objects.all().filter(agency=checking.count.agency).first()
            if (count.balance - withdraw) >= 0:
                count.balance -= withdraw 
            elif(count.balance + count.limit) - withdraw >= 0:
                count.balance -= withdraw
            else:
                messages.error(
                    self.request,
                    'Não foi permitiodo realizar o saque. Pois, o valor que você deseja sacar é superior ao permitido.'
                )
            count.save()
                

        if saving:
            count = Savings.objects.all().filter(agency=saving.count.agency).first()
            count.balance -= withdraw
            if (count.balance - withdraw) >= 0:
                count.balance -= withdraw
            else:
                messages.error(
                    self.request,
                    'O valor que você deseja sacar é superior ao permitido.'
                )
            count.save()
        
        if juridical:
            count = Legal.objects.all().filter(agency=juridical.count.agency).first()
            balance = count.balance
            if (count.balance - withdraw) > 0:
                count.balance -= withdraw 
            elif(count.balance + count.limit) - withdraw >= 0:
                count.balance -= withdraw
            else:
                messages.error(
                    self.request,
                    'O valor que você deseja sacar é superior ao permitido.'
                )
            count.save()

        return redirect('counts:withdraw')
