from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from counts.models import Checking, Legal, Savings
from . import models
from . import forms

class IndexView(View):
    template_name = 'profiles/index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

class CheckingView(View):
    template_name = 'profiles/checking.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Checking_Person.objects.filter(user=self.request.user).first()
            
            self.context = {
                'userForm': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
                'checkingPerson': forms.CheckingPersonForm(data=self.request.POST or None, instance=self.profile),
                'checkingCount': forms.CheckingForm(data=self.request.POST or None, instance=self.profile)
            }
        else:
            self.context = {
                'userForm': forms.UserForm(data=self.request.POST or None),
                'checkingPerson': forms.CheckingPersonForm(data=self.request.POST or None),
                'checkingCount': forms.CheckingForm(data=self.request.POST or None),
            }

        self.userForm = self.context['userForm']
        self.checkingPerson = self.context['checkingPerson']
        self.checkingCount = self.context['checkingCount']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *agrs, **kwargs):
        if not self.userForm.is_valid():
            return self.render
        else:
            username = self.userForm.cleaned_data.get('username')
            password = self.userForm.cleaned_data.get('password')
            email = self.userForm.cleaned_data.get('email')
            first_name = self.userForm.cleaned_data.get('first_name')
            last_name = self.userForm.cleaned_data.get('last_name')

            user = get_object_or_404(User, username=self.request.user.username)

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            if user.last_name:
                user.last_name = last_name
            user.save()
            
            if password:
                authenticates = authenticate(
                    self.request,
                    username=user,
                    password=password
                )

                if authenticates:
                    login(self.request, user=user)


        if not self.userForm.is_valid() or not self.checkingPerson.is_valid() or not self.checkingCount.is_valid():
            return self.render

        username = self.userForm.cleaned_data.get('username')
        password = self.userForm.cleaned_data.get('password')
        email = self.userForm.cleaned_data.get('email')
        first_name = self.userForm.cleaned_data.get('first_name')
        last_name = self.userForm.cleaned_data.get('last_name')
        
        # Logged user
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)

            user.username = username

            if password:
                user.set_password(password)

            user.email = email

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if password:
                authenticates = authenticate(
                    self.request,
                    username=user,
                    password=password,
                )

                if authenticates:
                    login(self.request, user=user)
                    redirect('profiles:details')

            if not self.profile:
                self.checkingPerson.cleaned_data['user'] = user
                profile = models.Checking_Person(**self.checkingPerson.cleaned_data)
                profile.save()
            else:
                profile = self.checkingPerson.save(commit=False)
                profile.user = user
                profile.save()

            redirect('profiles:index')

        # New user
        else:
            user = self.userForm.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.checkingPerson.save(commit=False)
            profile.user = user 
            count = self.checkingCount.save()
            profile.count = count
            profile.save()

        if password:
            authenticates = authenticate(
                self.request,
                username=user,
                password=password,
            )

            if authenticates:
                login(self.request, user=user)
        
        return redirect('profiles:index')

    def get(self, *args, **kwargs):
        return self.render

class JuridicalView(View):
    template_name = 'profiles/juridical.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Checking_Person.objects.filter(user=self.request.user).first()
            
            self.context = {
                'userJuridicalForm': forms.UserJuridicalForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
                'juridicalPerson': forms.JuridicalPersonForm(data=self.request.POST or None, instance=self.profile),
                'juridicalCount': forms.LegalForm(data=self.request.POST or None, instance=self.profile)
            }
        else:
            self.context = {
                'userJuridicalForm': forms.UserJuridicalForm(data=self.request.POST or None),
                'juridicalPerson': forms.JuridicalPersonForm(data=self.request.POST or None),
                'juridicalCount': forms.LegalForm(data=self.request.POST or None),
                'type': 'juridical',
            }

        self.userForm = self.context['userJuridicalForm']
        self.juridicalPerson = self.context['juridicalPerson']
        self.juridicalCount = self.context['juridicalCount']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *agrs, **kwargs):
        if not self.userForm.is_valid() or not self.juridicalPerson.is_valid() or not self.juridicalCount:
            return self.render

        username = self.userForm.cleaned_data.get('username')
        password = self.userForm.cleaned_data.get('password')
        email = self.userForm.cleaned_data.get('email')
        first_name = self.userForm.cleaned_data.get('first_name')
        last_name = self.userForm.cleaned_data.get('last_name')
        
        # Logged user
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)

            user.username = username

            if password:
                user.set_password(password)

            user.email = email

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.juridicalPerson.cleaned_data['user'] = user
                profile = models.Legal_Person(**self.juridicalPerson.cleaned_data)
                profile.save()
            else:
                profile = self.juridicalPerson.save(commit=False)
                profile.user = user
                profile.save()

            redirect('profiles:index')

        # New user
        else:
            user = self.userForm.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.juridicalPerson.save(commit=False)
            profile.user = user 
            count = self.juridicalCount.save()
            profile.count = count
            profile.save()

        if password:
            authenticates = authenticate(
                self.request,
                username=user,
                password=password,
            )

            if authenticates:
                login(self.request, user=user)
                
                
        return redirect('profiles:index')

    def get(self, *args, **kwargs):
        return self.render

class SavingsView(View):
    template_name = 'profiles/savings.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Checking_Person.objects.filter(user=self.request.user).first()
            
            self.context = {
                'userForm': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
                'savingsPerson': forms.SavingsPersonForm(data=self.request.POST or None),
                'savingsCount': forms.SavingsForm(data=self.request.POST or None)
            }
        else:
            self.context = {
                'userForm': forms.UserForm(data=self.request.POST or None),
                'savingsPerson': forms.SavingsPersonForm(data=self.request.POST or None),
                'savingsCount': forms.SavingsForm(data=self.request.POST or None),
                'type': 'savings',
            }

        self.userForm = self.context['userForm']
        self.savingsPerson = self.context['savingsPerson']
        self.savingsCount = self.context['savingsCount']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def post(self, *agrs, **kwargs):
        if not self.userForm.is_valid() or not self.savingsPerson.is_valid() or not self.savingsCount:
            return self.render

        username = self.userForm.cleaned_data.get('username')
        password = self.userForm.cleaned_data.get('password')
        email = self.userForm.cleaned_data.get('email')
        first_name = self.userForm.cleaned_data.get('first_name')
        last_name = self.userForm.cleaned_data.get('last_name')
        
        # Logged user
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)

            user.username = username

            if password:
                user.set_password(password)

            user.email = email

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.savingsPerson.cleaned_data['user'] = user
                profile = models.Savings_Person(**self.savingsPerson.cleaned_data)
                profile.save()
            else:
                profile = self.savingsPerson.save(commit=False)
                profile.user = user
                profile.save()
            
            redirect('profiles:index')

        # New user
        else:
            user = self.userForm.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.savingsPerson.save(commit=False)
            profile.user = user 
            count = self.savingsCount.save()
            profile.count = count
            profile.save()

        if password:
            authenticates = authenticate(
                self.request,
                username=user,
                password=password,
            )

            if authenticates:
                login(self.request, user=user)
        
        return redirect('profiles:index')

    def get(self, *args, **kwargs):
        return self.render

class LoginView(View):
    template_name = 'profiles/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos'
            )
            return redirect('profiles:login')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            messages.error(
                self.request,
                'Usuário ou senha inválidos'
            )
            return redirect('profiles:login')
       
        login(self.request, user=user)

        return redirect('profiles:index')

class LogoutView(View):
    def get(self, *args, **kwargs):

        logout(self.request)

        return redirect('profiles:index')

class DetailsView(View):
    template_name = 'profiles/details.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        user = self.request.user

        checking = models.Checking_Person.objects.all().filter(user=user).first()
        saving = models.Savings_Person.objects.all().filter(user=user).first()
        juridical = models.Legal_Person.objects.all().filter(user=user).first()

        count = None
        profile = None

        if checking:
            profile = models.Checking_Person.objects.all().filter(user=user).first()
            count = Checking.objects.all().filter(agency=checking.count.agency).first()

        if saving:
            profile = models.Savings_Person.objects.all().filter(user=user).first()
            count = Savings.objects.all().filter(agency=saving.count.agency).first()
        
        if juridical:
            profile = models.Legal_Person.objects.all().filter(user=user).first()
            count = Legal.objects.all().filter(agency=juridical.count.agency).first()

        self.context = {
            'user': user,
            'count':count,
            'profile': profile,
        }
       

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render
