# Generated by Django 5.1.3 on 2024-12-07 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('ReadyForPickUp', 'Ready for Pick Up'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
