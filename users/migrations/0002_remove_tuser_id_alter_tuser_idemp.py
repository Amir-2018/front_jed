# Generated by Django 4.2.3 on 2023-07-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='tuser',
            name='idemp',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
