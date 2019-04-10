from django.conf import settings # import the settings file

def name_of_app(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'APP_NAME': "CreatureCodex"}
