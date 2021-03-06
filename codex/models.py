from django.db import models

# Create your models here.

# When running into env issue in makemigrate...manually export settings file.
# export DJANGO_SETTINGS_MODULE=encounter.settings

# FIRST TESTS: m2m removed; only one dict field here...start by trying the TextField, then picklefield.

class Alignment(models.Model):

    # Fields
    alignment = models.CharField(max_length=128)

    def __str__(self,):

        return self.alignment

class HitDieType(models.Model):

    # Fields
    hitDieType = models.CharField(max_length=3)
    # d4, d6, d8, d10, d12

    def __str__(self,):

        return self.hitDieType

class Size(models.Model):

    # Fields
    size = models.CharField(max_length=24)

    def __str__(self,):

        return self.size

class Subtype(models.Model):

    # Fields
    subtype = models.CharField(max_length=128)

    def __str__(self,):

        return self.subtype

class Type(models.Model):

    # Fields
    type = models.CharField(max_length=128)

    def __str__(self,):

        return self.type

class ConditionImmunities(models.Model):

    # Fields
    conditionImmunity = models.CharField(max_length=256)
    # For numerous weirdly formatted explained ones, just throw them in here as strs separately.

    # The 'creatures' field will be filled in here by Creature

    def __str__(self,):

        return self.conditionImmunity

# For immunities, resistences, and vulnerabilities:
class DamageType(models.Model):

    # Fields
    damageType = models.CharField(max_length=256)
    # For numerous weirdly formatted explained ones, just throw them in here as strs separately.

    def __str__(self,):

        return self.damageType

class Languages(models.Model):

    # Fields
    language = models.CharField(max_length=256)

    def __str__(self,):

        return self.language

class Senses(models.Model):

    # Fields
    sense = models.CharField(max_length=128)

    def __str__(self,):

        return self.sense

class Speed(models.Model):

    # Fields
    speed = models.CharField(max_length=256)

    def __str__(self,):

        return self.speed

class Creature(models.Model):

    # Fields - Char
    name = models.CharField(max_length=128)

    # Fields - Ability scores and saves (Int)
    # Note that str was reserved, hence the Score for the raw abilities
    strScore =  models.IntegerField()
    strSave = models.IntegerField(null=True)
    dexScore = models.IntegerField()
    dexSave = models.IntegerField (null=True)
    conScore = models.IntegerField()
    conSave = models.IntegerField(null=True)
    intScore = models.IntegerField()
    intSave = models.IntegerField(null=True)
    wisScore = models.IntegerField()
    wisSave = models.IntegerField(null=True)
    chaScore = models.IntegerField()
    chaSave = models.IntegerField(null=True)

    # Fields - Skills (Int, all NULLable)
    arcana = models.IntegerField(null=True)
    athletics = models.IntegerField(null=True)
    deception = models.IntegerField(null=True)
    history = models.IntegerField(null=True)
    insight = models.IntegerField(null=True)
    intimidation = models.IntegerField(null=True)
    investigation = models.IntegerField(null=True)
    medicine = models.IntegerField(null=True)
    nature = models.IntegerField(null=True)
    perception = models.IntegerField(null=True)
    performance = models.IntegerField(null=True)
    persuasion = models.IntegerField(null=True)
    religion = models.IntegerField(null=True)
    stealth = models.IntegerField(null=True)
    survival = models.IntegerField(null=True)

    # Fields - Other monster-specific stats
    armorClass = models.IntegerField()
    challengeRating = models.FloatField()
    hitDieNum = models.IntegerField() # Gathered form the HD...
    hitPoints = models.IntegerField()
    passivePerception = models.IntegerField() # Gathered from Senses...
    proficiencyBonus = models.IntegerField() # Based on CR...

    # Fields - ForeignKeys...many creatures to one
    alignment = models.ForeignKey(Alignment,on_delete=models.CASCADE)
    hitDieType = models.ForeignKey(HitDieType,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    subtype = models.ForeignKey(Subtype,on_delete=models.CASCADE,null=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)

    # Fields - ForeignKeys...many-to-many
    conditionImmunities = models.ManyToManyField(ConditionImmunities,through='ConditionImmunitiesCreature',
                                                 #related_name='creatures',
                                                 )
    damageImmunities = models.ManyToManyField(DamageType,through='DamageImmunitiesCreature',related_name='immunity')
    damageResistances = models.ManyToManyField(DamageType,through='DamageResistancesCreature',related_name='resistance')
    damageVulnerabilities = models.ManyToManyField(DamageType,through='DamageVulnerabilitiesCreature',related_name='vulnerability')
    languages = models.ManyToManyField(Languages,through='LanguagesCreature') # Explanation area? Or just str...
    senses = models.ManyToManyField(Senses,through='SensesCreature')
    speed = models.ManyToManyField(Speed,through='SpeedCreature')

    def __str__(self,):

        # Curious if this will return the connected type...or just the type foreign key?
        return "{}, {}".format(self.name,self.type)


# Through tables for many-to-many:
#
# Note: For many-to-many relationships, simply define the two models on either side,
# then define the through table as a table with a foreign key to both. Neither of
# the sides should have any indication of the other...all their pairing info is stored
# in the through table. Furthermore, this means that NULLs are not needed whatsoever.
#
# Finally, since multiple m2m relationships have an endpoint at the DamageType table, the
# related_name of each must be different. I do not believe this shows up in the tables
# themselves anywhere...just an "under the hood" label.

class ConditionImmunitiesCreature(models.Model):

    conditionImmunity = models.ForeignKey(ConditionImmunities,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class DamageImmunitiesCreature(models.Model):

    damageImmunity = models.ForeignKey(DamageType,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class DamageResistancesCreature(models.Model):

    damageResistance = models.ForeignKey(DamageType,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class DamageVulnerabilitiesCreature(models.Model):

    damageVulnerability = models.ForeignKey(DamageType,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class LanguagesCreature(models.Model):

    language = models.ForeignKey(Languages,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class SensesCreature(models.Model):

    sense = models.ForeignKey(Senses,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

class SpeedCreature(models.Model):

    speed = models.ForeignKey(Speed,on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

# Fields - Text: one (creature)-to-many (actions)

class Action_Name(models.Model):

    # Fields
    name = models.CharField(max_length=128)

    def __str__(self,):

        return self.name

class Actions(models.Model):

    # Fields
    name = models.ForeignKey(Action_Name,on_delete=models.CASCADE)
    desc = models.TextField()
    damageDice = models.CharField(max_length=8,null=True)
    damageBonus = models.IntegerField(null=True)
    attackBonus = models.IntegerField()
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

    def __str__(self,):

        return self.name

class LegendaryActions(models.Model):

    # Fields
    name = models.ForeignKey(Action_Name,on_delete=models.CASCADE)
    desc = models.TextField()
    damageDice = models.CharField(max_length=8,null=True)
    attackBonus = models.IntegerField()
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

    def __str__(self,):

        return self.name

class Reactions(models.Model):

    # Fields
    name = models.ForeignKey(Action_Name,on_delete=models.CASCADE)
    desc = models.TextField()
    attackBonus = models.IntegerField()
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

    def __str__(self,):

        return self.name

class SpecialAbilities(models.Model):

    # Fields
    name = models.ForeignKey(Action_Name,on_delete=models.CASCADE)
    desc = models.TextField()
    damageDice = models.CharField(max_length=8,null=True)
    attackBonus = models.IntegerField()
    creature = models.ForeignKey(Creature,on_delete=models.CASCADE)

    def __str__(self,):

        return self.name
