# Generated by Django 2.1.7 on 2019-03-26 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0007_specialabilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionImmunities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conditionImmunity', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ConditionImmunitiesCreature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conditionImmunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.ConditionImmunities')),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature')),
            ],
        ),
        migrations.RenameModel(
            old_name='Rections',
            new_name='Reactions',
        ),
        migrations.AddField(
            model_name='creature',
            name='conditionImmunities',
            field=models.ManyToManyField(null=True, through='codex.ConditionImmunitiesCreature', to='codex.ConditionImmunities'),
        ),
    ]