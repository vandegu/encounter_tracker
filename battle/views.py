from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.mixins import LoginRequiredMixin

from battle.models import *
from codex.models import *

# Create your views here.

class BattleDetailView(LoginRequiredMixin, View):
    model = EncounterInstance
    template_name = 'battle/battle_detail.html'

class BattleCreateView(LoginRequiredMixin, View):
    template = 'battle/battle_form.html'
    success_url = reverse_lazy('battle_create')

    def get(self, request, pk=None):
        creatures = Creature.objects.all()
        context = {'creature_list' : creatures}
        return render(request,self.template,context)

    def post(self, request, pk=None):
        print(request.POST)
        # if request.POST['encounterName'].strip() == '':
        #     print('BAD BAAD BAAAD')
        #     return render(request,reverse_lazy('battle_create'),{'validationError' : "Must have non-empty encounter name!"})

        # Separate the name from the creatures and CSRF token...
        name = request.POST['encounterName']
            # This is really strange...it asked for owner_id (no field named owner_id), but then labeled it owner_id_id)
        ei = EncounterInstance(name=name,owner_id=self.request.user)
        ei.save()

        # Separate the creatures from the rest now...
        for item in list(request.POST.keys())[2:]:
            creature_name = item.split('-')[0].replace('_',' ')
            creature = Creature.objects.get(name=creature_name)
            cr = CreatureInstance(creature=creature,
                currentHitPoints = getattr(creature,'hitPoints'),
                maxHitPoits = getattr(creature,'hitPoints'),
                ac = getattr(creature, "armorClass"),
                encounter = ei
            )
            cr.save()

        # Create Encounter instance in the db.

        return redirect(self.success_url)

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