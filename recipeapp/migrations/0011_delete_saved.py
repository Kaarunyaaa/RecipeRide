# Generated by Django 4.2.5 on 2024-09-07 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0010_saves'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Saved',
        ),
    ]