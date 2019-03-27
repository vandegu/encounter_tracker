# Code to run through the django manage shell as below to populate database.
#
# python3 manage.py shell < load_entries.py

import json
import os
import re
import codex.models as cm

qqq = open('damages.txt','w')

# https://stackoverflow.com/questions/7584418/iterate-the-classes-defined-in-a-module-imported-dynamically
classes = dict([(name, cls) for name, cls in cm.__dict__.items() if isinstance(cls, type)])

# Clear database (not the tables and migrations, just the data, and only from
# the models that are defined in codex.models.py)
print('\n')
for cl in classes:
    print("CLEARING TABLE {}...".format(cl))
    classes[cl].objects.all().delete()
print('\n')

# Open .json
with open('./dnd_monsters.json') as f:
    entries = json.loads(f.read())

# Remove the license and save
license = entries.pop(-1)

# CR stuff:
# CR-parsing function...
def convertCR(s):
    import re
    a = re.findall(r"[0-9]+",s)
    if len(a) == 1:
        return float(a[0])
    elif len(a) == 2:
        return float(a[0])/float(a[1])
    else:
        print("Error in parsing Challenge Rating.")
# CR-proficiency conversion dict...
CRconv = dict(zip([0,0.125,0.25,0.5,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
                  [2,2,2,2,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9]))

# Every field in the json...this is used when we chack the Creature entries for NULLs...
fields = ['acrobatics', 'actions', 'alignment', 'arcana', 'armor_class',
       'athletics', 'challenge_rating', 'charisma', 'charisma_save',
       'condition_immunities', 'constitution', 'constitution_save',
       'damage_immunities', 'damage_resistances', 'damage_vulnerabilities',
       'deception', 'dexterity', 'dexterity_save', 'history', 'hit_dice',
       'hit_points', 'insight', 'intelligence', 'intelligence_save',
       'intimidation', 'investigation', 'languages', 'legendary_actions',
       'medicine', 'nature', 'perception', 'performance',
       'persuasion', 'reactions', 'religion', 'senses', 'size',
       'special_abilities', 'speed', 'stealth', 'strength', 'strength_save',
       'subtype', 'survival', 'type', 'wisdom', 'wisdom_save']

# Loop through entries, look to see if the object has already occured in the DB,
# if not, get it and update the DB. Start with the ForeignKeys.
print('Entering monsters...\n')
for e in entries[:]:

    # Get HD for split (0 for full, 1 for first group, 2 for second group)
    HD = re.match(r"(.+)(d.+)",e['hit_dice'])
    #print(HD.group(2))

    # Get passive perception: Need to use Findall here, because match only matches
    # from the FRONT of the string. Keep in mind that Findall returns a list of matched
    # groups.
    PP = re.findall(r"passive Perception\W+([0-9]+)",e['senses'])
    #print(e['senses'],PP[0])


    try:
        alignment = cm.Alignment.objects.get(alignment=e['alignment'])
    except:
        print("Inserting 1-M alignment {}...".format(e['alignment']))
        # I'd like to more fully understand what's happening in the below 2 lines...
        alignment = cm.Alignment(alignment=e['alignment'])
        alignment.save()

    try:
        hitDieType = cm.HitDieType.objects.get(hitDieType=HD.group(2))
    except:
        print("Inserting 1-M hit-die type {}...".format(HD.group(2)))
        # I'd like to more fully understand what's happening in the below 2 lines...
        hitDieType = cm.HitDieType(hitDieType=HD.group(2))
        hitDieType.save()

    try:
        size = cm.Size.objects.get(size=e['size'])
    except:
        print("Inserting 1-M size {}...".format(e['size']))
        # I'd like to more fully understand what's happening in the below 2 lines...
        size = cm.Size(size=e['size'])
        size.save()

    # Subtypes are included in each entry, just some are already None.
    try:
        subtype = cm.Subtype.objects.get(subtype=e['subtype'])
    except:
        print("Inserting 1-M subtype {}...".format(e['subtype']))
        # I'd like to more fully understand what's happening in the below 2 lines...
        subtype = cm.Subtype(subtype=e['subtype'])
        subtype.save()

    try:
        type = cm.Type.objects.get(type=e['type'])
    except:
        print("Inserting 1-M type {}...".format(e['type']))
        # I'd like to more fully understand what's happening in the below 2 lines...
        type = cm.Type(type=e['type'])
        type.save()

    # Get monster entries. Carriage return after name is intentional...attaches the
    # above added entries to the creature.
    print("CREATURE ENTRY: {}".format(e['name']))

    # Check for fields with no entry, if so, give them an entry of None to convert to NULL in DB...

    for field in fields:
        if field in e:
            continue
        else:
            e[field] = None

    creature = cm.Creature(name = e['name'],

                           # ability scores and saves

                           strScore = e['strength'],
                           strSave = e['strength_save'],
                           dexScore = e['dexterity'],
                           dexSave = e['dexterity_save'],
                           conScore = e['constitution'],
                           conSave = e['constitution_save'],
                           intScore = e['intelligence'],
                           intSave = e['intelligence_save'],
                           wisScore = e['wisdom'],
                           wisSave = e['wisdom_save'],
                           chaScore = e['charisma'],
                           chaSave = e['charisma_save'],

                           # skills

                           arcana = e['arcana'],
                           athletics = e['athletics'],
                           deception = e['deception'],
                           history = e['history'],
                           insight = e['insight'],
                           intimidation = e['intimidation'],
                           investigation = e['investigation'],
                           medicine = e['medicine'],
                           nature = e['nature'],
                           perception = e['perception'],
                           performance = e['performance'],
                           persuasion = e['persuasion'],
                           religion = e['religion'],
                           stealth = e['stealth'],
                           survival = e['survival'],

                           # other specific stats

                           armorClass = e['armor_class'],
                           challengeRating = convertCR(e['challenge_rating']),
                           hitDieNum = HD.group(1),
                           hitPoints = e['hit_points'],
                           passivePerception = PP[0],
                           proficiencyBonus = CRconv[convertCR(e['challenge_rating'])],

                           # many-to-one keys

                           alignment = alignment,
                           hitDieType = hitDieType,
                           size = size,
                           subtype = subtype,
                           type = type,
                        )

    creature.save()

    # Get the Actions...make entries for them and their dependencies...
    if 'actions' in e and e['actions'] != None:
        for action in e['actions']:

            # Check the NULLS...
            for check in ['damage_bonus','damage_dice']:
                if check in action:
                    continue
                else:
                    action[check] = None

            try:
                aname = cm.Action_Name.objects.get(name=action['name'])
            except:
                print("Inserting M-1 action_name {}...".format(action['name']))
                # I'd like to more fully understand what's happening in the below 2 lines...
                aname = cm.Action_Name(name=action['name'])
                aname.save()

            act = cm.Actions(name = aname,
                             desc = action['desc'],
                             damageDice = action['damage_dice'],
                             damageBonus = action['damage_bonus'],
                             attackBonus = action['attack_bonus'],
                             creature = creature
                             )

            act.save()

    if 'legendary_actions' in e and e['legendary_actions'] != None:
        for action in e['legendary_actions']:

            # Check the NULLS...
            for check in ['damage_dice']:
                if check in action:
                    continue
                else:
                    action[check] = None

            try:
                aname = cm.Action_Name.objects.get(name=action['name'])
            except:
                print("Inserting M-1 legendary action_name {}...".format(action['name']))
                # I'd like to more fully understand what's happening in the below 2 lines...
                aname = cm.Action_Name(name=action['name'])
                aname.save()

            act = cm.LegendaryActions(name = aname,
                             desc = action['desc'],
                             damageDice = action['damage_dice'],
                             attackBonus = action['attack_bonus'],
                             creature = creature
                             )

            act.save()

    if 'reactions' in e and e['reactions'] != None:
        for action in e['reactions']:

            try:
                aname = cm.Action_Name.objects.get(name=action['name'])
            except:
                print("Inserting M-1 reaction_name {}...".format(action['name']))
                # I'd like to more fully understand what's happening in the below 2 lines...
                aname = cm.Action_Name(name=action['name'])
                aname.save()

            act = cm.Reactions(name = aname,
                             desc = action['desc'],
                             attackBonus = action['attack_bonus'],
                             creature = creature
                             )

            act.save()

    if 'special_abilities' in e and e['special_abilities'] != None:
        for action in e['special_abilities']:

            # Check the NULLS...
            for check in ['damage_dice']:
                if check in action:
                    continue
                else:
                    action[check] = None

            try:
                aname = cm.Action_Name.objects.get(name=action['name'])
            except:
                print("Inserting M-1 special ability action_name {}...".format(action['name']))
                # I'd like to more fully understand what's happening in the below 2 lines...
                aname = cm.Action_Name(name=action['name'])
                aname.save()

            act = cm.SpecialAbilities(name = aname,
                             desc = action['desc'],
                             damageDice = action['damage_dice'],
                             attackBonus = action['attack_bonus'],
                             creature = creature
                             )

            act.save()

    # Get the many-to-many's:
    #
    # I think the through table will keep track most of this info, and there is no
    # way or need to have this info present on either table. In other words, it is
    # not necessary for the creatures to know what conditions, or the conditions to
    # know their creatures, because this info is stored by the through table. So,
    # just use this to define the immunities from each creature!

    if 'condition_immunities' in e and e['condition_immunities'] != None:
        cis = re.findall(r'(\w+)',e['condition_immunities'])
        for ci in cis:
            try:
                conditionImmunity = cm.ConditionImmunities.objects.get(conditionImmunity=ci)
            except:
                print("Inserting M-M condition immunity {}...".format(ci))
                # I'd like to more fully understand what's happening in the below 2 lines...
                conditionImmunity = cm.ConditionImmunities(conditionImmunity=ci)
                conditionImmunity.save()

            # Create entry in through table now.
            zz = cm.ConditionImmunitiesCreature(conditionImmunity = conditionImmunity,
                                                creature = creature)

            zz.save()

    if 'damage_immunities' in e and e['damage_immunities'] != None and e['damage_immunities'] != '':
        if re.search(r'from',e['damage_immunities']):
            a = e['damage_immunities'].split('; ')
            if len(a)>1:
                out = a[0].split(', ')
                cis = out+a[1:]
            else:
                cis = a
        else:
            cis = e['damage_immunities'].split(', ')
            # qqq.write(e['damage_immunities']+'\n')
            # for zzz in cis:
            #     qqq.write('{}|'.format(zzz))
            # qqq.write('\n\n\n')
        for ci in cis:
            try:
                damageImmunity = cm.DamageType.objects.get(damageType=ci)
            except:
                print("Inserting M-M damage immunity {}...".format(ci))
                # I'd like to more fully understand what's happening in the below 2 lines...
                damageImmunity = cm.DamageType(damageType=ci)
                damageImmunity.save()

            # Create entry in through table now.
            zz = cm.DamageImmunitiesCreature(damageImmunity = damageImmunity,
                                                creature = creature)

            zz.save()

    if 'damage_resistances' in e and e['damage_resistances'] != None and e['damage_resistances'] != '':
        if re.search(r'from',e['damage_resistances']):
            a = e['damage_resistances'].split('; ')
            if len(a)>1:
                out = a[0].split(', ')
                cis = out+a[1:]
            else:
                cis = a
        else:
            cis = e['damage_resistances'].split(', ')
            # qqq.write(e['damage_immunities']+'\n')
            # for zzz in cis:
            #     qqq.write('{}|'.format(zzz))
            # qqq.write('\n\n\n')
        for ci in cis:
            try:
                damageResistance = cm.DamageType.objects.get(damageType=ci)
            except:
                print("Inserting M-M damage resistance {}...".format(ci))
                # I'd like to more fully understand what's happening in the below 2 lines...
                damageResistance = cm.DamageType(damageType=ci)
                damageResistance.save()

            # Create entry in through table now.
            zz = cm.DamageResistancesCreature(damageResistance = damageResistance,
                                                creature = creature)

            zz.save()

    if 'damage_vulnerabilities' in e and e['damage_vulnerabilities'] != None and e['damage_vulnerabilities'] != '':
        if re.search(r'from',e['damage_vulnerabilities']):
            a = e['damage_vulnerabilities'].split('; ')
            if len(a)>1:
                out = a[0].split(', ')
                cis = out+a[1:]
            else:
                cis = a
        else:
            cis = e['damage_vulnerabilities'].split(', ')
            # qqq.write(e['damage_immunities']+'\n')
            # for zzz in cis:
            #     qqq.write('{}|'.format(zzz))
            # qqq.write('\n\n\n')
        for ci in cis:
            try:
                damageVulnerability = cm.DamageType.objects.get(damageType=ci)
            except:
                print("Inserting M-M damage vulnerability {}...".format(ci))
                # I'd like to more fully understand what's happening in the below 2 lines...
                damageVulnerability = cm.DamageType(damageType=ci)
                damageVulnerability.save()

            # Create entry in through table now.
            zz = cm.DamageVulnerabilitiesCreature(damageVulnerability = damageVulnerability,
                                                creature = creature)

            zz.save()


    print('\n')
