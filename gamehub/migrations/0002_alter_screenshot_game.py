# Generated by Django 3.2.7 on 2021-09-21 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamehub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='gamehub.game'),
        ),
    ]
