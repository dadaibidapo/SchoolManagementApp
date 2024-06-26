# Generated by Django 4.2.7 on 2024-04-23 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0002_alter_class_class_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.RenameField(
            model_name='class',
            old_name='name',
            new_name='class_name',
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrators.department')),
            ],
        ),
    ]
