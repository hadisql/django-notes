# Generated by Django 4.2.2 on 2023-07-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previousavatar',
            name='image',
            field=models.ImageField(upload_to='avatars/'),
        ),
    ]