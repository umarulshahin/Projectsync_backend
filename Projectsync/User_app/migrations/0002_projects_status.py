# Generated by Django 5.1.4 on 2024-12-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='status',
            field=models.CharField(choices=[('planned', 'planned'), ('active', 'active'), ('Completed', 'Completed')], default='planned', max_length=100),
        ),
    ]
