# Generated by Django 2.2 on 2019-04-12 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encounterinstance',
            old_name='owner',
            new_name='owner_id',
        ),
    ]