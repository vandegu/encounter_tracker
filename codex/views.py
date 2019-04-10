from django.views import View
from django.views import generic
from django.shortcuts import render

from codex.models import *

# Create your views here.

class CreatureListView(generic.ListView):
    model = Creature

    # paginate_by = 20

class CreatureDetailView(generic.DetailView):
    model = Creature
    template_name = "codex/creature_detail.html"

    def get(self, request, pk) :
        # Below line is necessary because the get_context_data method uses the object
        # to pass it into the context. Below is the reference.
        # https://stackoverflow.com/questions/34460708/checkoutview-object-has-no-attribute-object
        self.object = self.get_object()
        context = super(CreatureDetailView, self).get_context_data()
        c = Creature.objects.get(id=pk)
        ability_matrix = [['STR',c.strScore,c.strSave],
                            ['DEX',c.dexScore,c.dexSave],
                            ['CON',c.conScore,c.conSave],
                            ['INT',c.intScore,c.intSave],
                            ['WIS',c.wisScore,c.wisSave],
                            ['CHA',c.chaScore,c.chaSave]]
        # Replaces the printouts of None with actually nothing by checking if there is anything
        # actually in the matrix at each location.
        # https://stackoverflow.com/questions/12507281/determine-empty-template-variable-in-django
        context['abilities'] = [[value if value else '' for value in row] for row in ability_matrix]

        # skills
        skills = []
        sk_names = ['Arcana','Athletics','Deception','History','Insight','Intimidation','Invesitgation',
                    'Medicine','Nature','Perception','Performance','Persuasion','Religion','Stealth',
                    'Survival']
        for i,sk in enumerate([c.arcana,c.athletics,c.deception,c.history,c.insight,c.intimidation,c.investigation,
                   c.medicine,c.nature,c.perception,c.performance,c.persuasion,c.religion,c.stealth,
                   c.survival]):
            if sk:
                skills.append([sk_names[i],sk])
        context['skills'] = skills
        return render(request, self.template_name, context)
