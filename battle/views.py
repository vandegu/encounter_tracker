from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from battle.models import *
from codex.models import *

# Create your views here.

class BattleCreateView(LoginRequiredMixin, View):
    template = 'battle/battle_form.html'
    success_url = reverse_lazy('battle_create')

    def get(self, request, pk=None):
        creatures = Creature.objects.all()
        context = {'creature_list' : creatures}
        return render(request,self.template,context)
    # def get(self, request, pk=None) :
    #     form = CreateForm()
    #     ctx = { 'form': form }
    #     return render(request, self.template, ctx)
    #
    # def post(self, request, pk=None) :
    #     form = CreateForm(request.POST, request.FILES or None)
    #
    #     if not form.is_valid() :
    #         ctx = {'form' : form}
    #         return render(request, self.template, ctx)
    #
    #     # Add owner to the model before saving
    #      = form.save(commit=False)
    #     ad.owner = self.request.user
    #     ad.save()
    #     return redirect(self.success_url)
