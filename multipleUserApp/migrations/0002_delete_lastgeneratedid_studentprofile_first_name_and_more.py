# Generated by Django 5.0.2 on 2024-04-16 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multipleUserApp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LastGeneratedID',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
