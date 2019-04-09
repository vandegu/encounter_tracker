# Generated by Django 2.1.7 on 2019-03-27 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0012_auto_20190327_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='LanguagesCreature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Languages')),
            ],
        ),
        migrations.AddField(
            model_name='creature',
            name='languages',
            field=models.ManyToManyField(through='codex.LanguagesCreature', to='codex.Languages'),
        ),
    ]