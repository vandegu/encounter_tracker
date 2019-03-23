from django.db import models

# Create your models here.

# When running into env issue in makemigrate...manually export settings file.
# export DJANGO_SETTINGS_MODULE=encounter.settings

# FIRST TESTS: m2m removed; only one dict field here...start by trying the TextField, then picklefield.

class Alignment(models.Model):

    # Fields
    alignment = models.CharField(max_length=128)

    def __str__(self,):

        return alignment

class HitDieType(models.Model):

    # Fields
    hitDieType = models.CharField(max_length=3)
    # d4, d6, d8, d10, d12

    def __str__(self,):

        return hitDieType

class Size(models.Model):

    # Fields
    size = models.CharField(max_length=24)

    def __Str__(self,):

        return size

class Subtype(models.Model):

    # Fields
    subtype = models.CharField(max_length=128)

    def __Str__(self,):

        return subtype

class Type(models.Model):

    # Fields
    type = models.CharField(max_length=128)

    def __str__(self,):

        return type

# class ConditionImmunities(models.Model):
#
#     # Fields
#     conditionImmunity = models.CharField(max_length=256)
#     # For numerous weirdly formatted explained ones, just throw them in here as strs separately.
#
#     def __str__(self,):
#
#         return conditionImmunity
#
# class DamageImmunities(models.Model):
#
#     # Fields
#     damageImmunity = models.CharField(max_length=256)
#     # For numerous weirdly formatted explained ones, just throw them in here as strs separately.
#
#     def __str__(self,):
#
#         return damageImmunity
#
# class DamageResistances(models.Model):
#
#     # Fields
#     damageResistance = models.CharField(max_length=256)
#
#     def __str__(self,):
#
#         return damageResistance
#
# class DamageVulnerabilities(models.Model):
#
#     # Fields
#     damageVulnerability = models.CharField(max_length=256)
#
#     def __Str__(sef,):
#
#         return damageVulnerability
#
# class Languages(models.Model):
#
#     # Fields
#     language = models.CharField(max_length=256)
#
#     def __str__(self,):
#
#         return language
# class Senses(models.Model):
#
#     # Fields
#     sense = models.CharField(max_length=256)
#
#     def __str__(self,):
#
#         return sense
#
# class Speed(models.Model):
#
#     # Fields
#     speed = models.CharField(max_length=256)
#
#     def __str__(self,):
#
#         return speed



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

    # Fields - ForeignKeys...one-to-many
    alignment = models.ForeignKey(Alignment,on_delete=models.CASCADE)
    hitDieType = models.ForeignKey(HitDieType,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    subtype = models.ForeignKey(Subtype,on_delete=models.CASCADE,null=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)

    # # Fields - ForeignKeys...many-to-many
    # conditionImmunities = models.ManyToManyField(ConditionImmunities,null=True)
    # damageImmunities = models.ManyToManyField(DamageImmunities,null=True)
    # damageResistances = models.ManyToManyField(DamageResistances,null=True)
    # damageVulnerabilities = models.ManyToManyField(DamageVulnerabilities,null=True)
    # languages = models.ManyToManyField(Languages,null=True) # Explanation area? Or just str...
    # senses = models.ManyToManyField(Senses,null=True)
    # speed = models.ManyToManyField(Speed)

    def __str__(self,):

        # Curious if this will return the connected type...or just the type foreign key?
        return "{}, {}".format(self.name,self.type)


# Fields - Text one (creature)-to-many (actions)

# actions = models.TextField(null=True)
# legendaryActions = models.TextField(null=True)
# reactions = models.TextField(null=True)
# specialAbilities = models.TextField(null=True)

class Actions(models.Model):

    # Fields
    name = ForeignKey(Action_Name,on_delete=models.CASCADE)
    desc = TextField()
    damageDice = CharField(max_length=8)
    damageBonus = CharField(max_length=8)
