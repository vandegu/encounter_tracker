# Generated by Django 2.1.7 on 2019-03-27 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0010_auto_20190326_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageResistancesCreature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='creature',
            name='damageImmunities',
            field=models.ManyToManyField(related_name='immunity', through='codex.DamageImmunitiesCreature', to='codex.DamageType'),
        ),
        migrations.AddField(
            model_name='damageresistancescreature',
            name='creature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature'),
        ),
        migrations.AddField(
            model_name='damageresistancescreature',
            name='damageResistance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.DamageType'),
        ),
        migrations.AddField(
            model_name='creature',
            name='damageResistances',
            field=models.ManyToManyField(related_name='resistance', through='codex.DamageResistancesCreature', to='codex.DamageType'),
        ),
    ]
