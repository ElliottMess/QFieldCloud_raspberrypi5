# Generated by Django 2.2.6 on 2020-03-12 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_fileversion_absolute_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='absolute_path',
            new_name='original_path',
        ),
        migrations.RenameField(
            model_name='fileversion',
            old_name='absolute_path',
            new_name='stored_path',
        ),
    ]
