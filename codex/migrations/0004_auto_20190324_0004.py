# Generated by Django 2.1.7 on 2019-03-24 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0003_auto_20190323_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='damageBonus',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='actions',
            name='damageDice',
            field=models.CharField(max_length=8, null=True),
        ),
    ]