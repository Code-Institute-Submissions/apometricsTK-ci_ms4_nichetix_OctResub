# Generated by Django 3.2.6 on 2021-09-29 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_location'),
        ('tickets', '0004_tickettype_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettype',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ticket_types', to='events.event'),
        ),
    ]