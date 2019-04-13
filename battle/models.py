from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class EncounterInstance(models.Model):
    name = models.CharField(max_length=256)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self,):
        return self.name

# The idea here is as follows:
#
# When the battle is created, a user will select which creatures will participate.
# Then, the form/view will save a creature instance for each creature chosen, and
# will look up the max HP and AC for each creature and save them into the db here.
class CreatureInstance(models.Model):
    creature = models.ForeignKey('codex.Creature',on_delete=models.CASCADE)
    currentHitPoints = models.IntegerField(null=True)
    maxHitPoits = models.IntegerField(null=True)
    ac = models.IntegerField(null=True)
    init = models.IntegerField(null=True)
    encounter = models.ForeignKey(EncounterInstance,on_delete=models.CASCADE,null=True)
