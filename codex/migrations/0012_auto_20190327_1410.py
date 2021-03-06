# Generated by Django 2.1.7 on 2019-03-27 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0011_auto_20190327_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageVulnerabilitiesCreature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature')),
                ('damageVulnerability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.DamageType')),
            ],
        ),
        migrations.AddField(
            model_name='creature',
            name='damageVulnerabilities',
            field=models.ManyToManyField(related_name='vulnerability', through='codex.DamageVulnerabilitiesCreature', to='codex.DamageType'),
        ),
    ]
