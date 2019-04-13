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

class BattleDetailView(LoginRequiredMixin,generic.DetailView):
    model = EncounterInstance
    template_name = 'battle/battle_detail.html'

    # Do a def get and obj or 404 here to make sure owner is the one viewing this page.
    def get(self, request, pk):
        encounterinstance = get_object_or_404(EncounterInstance, id=pk, owner_id=self.request.user)
        context = {'encounterinstance' : encounterinstance}
        return render(request, self.template_name, context)

    def post(self,request,pk):
        #success_url = reverse_lazy('battle_detail', kwargs={'pk': pk})
        print(request.POST)

        # Loop through all of the fields retrieved except the CSRF token, parse them, and update database.
        for item in list(request.POST.keys())[1:]:
            items = item.split('-')
            field = items[0]
            creatureInstance_id = items[1]
            creatureInstance = CreatureInstance.objects.get(id=creatureInstance_id)
            if field == 'ini':
                creatureInstance.init = request.POST[item]
            elif field == 'chp':
                creatureInstance.currentHitPoints = request.POST[item]
            elif field == 'col':
                creatureInstance.color = request.POST[item]
            creatureInstance.save()

        encounterinstance = get_object_or_404(EncounterInstance, id=pk, owner_id=self.request.user)
        context = {'encounterinstance' : encounterinstance}

        return render(request,self.template_name,context)


class BattleCreateView(LoginRequiredMixin, View):
    template = 'battle/battle_form.html'
    success_url = reverse_lazy('battle_create')

    def get(self, request, pk=None):
        creatures = Creature.objects.all()
        context = {'creature_list' : creatures}
        return render(request,self.template,context)

    def post(self, request, pk=None):
        print(request.POST)
        if request.POST['encounterName'].strip() == '':
            creatures = Creature.objects.all()
            context = {'creature_list' : creatures,
                'validationError' : "Must have non-empty encounter name!"}
            return render(request,self.template,context)

        # Separate the name from the creatures and CSRF token...
        name = request.POST['encounterName']
            # This is really strange...it asked for owner_id (no field named owner_id), but then labeled it owner_id_id)
        ei = EncounterInstance(name=name,owner_id=self.request.user)
        ei.save()

        # Separate the creatures from the rest now...
        for item in list(request.POST.keys())[2:]:
            for i in range(int(request.POST[item])):
                creature_name = item.split('-')[0].replace('_',' ')
                creature = Creature.objects.get(name=creature_name)
                cr = CreatureInstance(creature=creature,
                    currentHitPoints = getattr(creature,'hitPoints'),
                    maxHitPoits = getattr(creature,'hitPoints'),
                    ac = getattr(creature, "armorClass"),
                    init = 0,
                    color = '#000000',
                    encounter = ei
                )
                cr.save()

        # Create Encounter instance in the db.

        return redirect(self.success_url)

class BattleDeleteView(LoginRequiredMixin,View):
    # I'll just make it myself instead of inheriting from the generic delete view.
    model = EncounterInstance
    template_name = "battle/battle_delete.html"

    def get(self, request, pk):
        encounterinstance = get_object_or_404(EncounterInstance, id=pk, owner_id=self.request.user)
        context = {'deleted_name' : encounterinstance.name}
        encounterinstance.delete()
        return render(request,self.template_name,context)
