# Generated by Django 3.2.7 on 2021-10-31 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='neighbourhood',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.neighbourhood'),
        ),
    ]
