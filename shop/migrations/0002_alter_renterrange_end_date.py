# Generated by Django 5.1.3 on 2024-11-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="renterrange",
            name="end_date",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
