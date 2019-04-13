from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re

from battle.models import *


# Create your views here.

class HomeView(View):
    def get(self, request):

        ctx = {}
        ctx['encounters'] = EncounterInstance.objects.all()
        ctx['userid'] = self.request.user.id

        return render(request, 'main_home.html', ctx)

class CreateUser(View):

    def get(self,request):
        return render(request,'registration/create_user.html')

    def post(self,request):
        username = request.POST['username']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']

        regexp = re.compile(r'\W')
        valid = True
        ctx = {}
        # Validate (must be longer than three characters each):
        if len(username) < 3 or regexp.search(username):
            valid = False
            ctx['uError'] = "Username must be at least three characters and cannot contain whitespace!"
        if len(password1) < 3 or regexp.search(password1) or password1 != password2:
            valid = False
            ctx['pError'] = "Password must be at least three characters and cannot contain whitespace, and your passwords must match!"

        if valid:
            user = User.objects.create_user(username=username,password=password1)
            user.save()

            user = authenticate(username = username, password = password1)
            if user is not None:
                login(request, user)

            return render(request,'main_home.html')

        else:
            print(ctx)
            return render(request,'registration/create_user.html',ctx)
