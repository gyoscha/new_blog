# Generated by Django 4.0.6 on 2022-08-21 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0008_note_read_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='read_user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='read_posts',
        ),
        migrations.AddField(
            model_name='note',
            name='read_posts',
            field=models.ManyToManyField(blank=True, to='blog_api.profile'),
        ),
    ]
