# Generated by Django 3.2.5 on 2021-07-30 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210730_0242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='user',
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='name',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]