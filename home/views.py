from django.shortcuts import render
from django.views import View
from django.conf import settings

from battle.models import *


# Create your views here.

class HomeView(View):
    def get(self, request):

        ctx = {}
        ctx['encounters'] = EncounterInstance.objects.all()
        ctx['userid'] = self.request.user.id 

        return render(request, 'main_home.html', ctx)
