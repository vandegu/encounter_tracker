# Generated by Django 2.1.7 on 2019-03-23 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0002_auto_20190323_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action_Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('damageDice', models.CharField(max_length=8)),
                ('damageBonus', models.IntegerField()),
                ('attackBonus', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='creature',
            name='actions',
        ),
        migrations.AddField(
            model_name='actions',
            name='creature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Creature'),
        ),
        migrations.AddField(
            model_name='actions',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.Action_Name'),
        ),
    ]
