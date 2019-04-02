from django.views import View
from django.views import generic
from django.shortcuts import render

from codex.models import *

# Create your views here.

class CreatureListView(generic.ListView):
    model = Creature
