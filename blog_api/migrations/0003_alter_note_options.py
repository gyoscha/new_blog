# Generated by Django 4.0.6 on 2022-08-03 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0002_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['create_at']},
        ),
    ]