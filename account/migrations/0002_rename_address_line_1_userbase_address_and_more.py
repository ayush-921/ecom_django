# Generated by Django 4.2.2 on 2023-07-13 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbase',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='userbase',
            name='address_line_2',
        ),
    ]
