# Generated by Django 2.1.7 on 2019-03-24 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0005_legendaryactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('attackBonus', models.IntegerField()),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Action_Name')),
            ],
        ),
    ]
