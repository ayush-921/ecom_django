# Generated by Django 4.2.2 on 2023-07-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userbase_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
