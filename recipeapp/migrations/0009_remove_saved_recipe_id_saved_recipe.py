# Generated by Django 4.2.5 on 2024-09-07 07:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0008_saved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saved',
            name='recipe_id',
        ),
        migrations.AddField(
            model_name='saved',
            name='recipe',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='recipeapp.addrecipe'),
            preserve_default=False,
        ),
    ]
