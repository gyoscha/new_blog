# Generated by Django 4.0.6 on 2022-08-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0005_note_read_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='read_by',
        ),
        migrations.AddField(
            model_name='note',
            name='read_by',
            field=models.ManyToManyField(blank=True, to='blog_api.profile'),
        ),
    ]
