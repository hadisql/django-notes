# Generated by Django 4.2.2 on 2023-06-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_notes_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['created_time']},
        ),
        migrations.AlterField(
            model_name='note',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
