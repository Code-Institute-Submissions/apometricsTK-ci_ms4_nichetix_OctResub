# Generated by Django 3.2.6 on 2021-09-21 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='order_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='checkout.orderitem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='tickets.tickettype'),
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='tax',
            field=models.CharField(choices=[('base', 19.0), ('cut', 7.0), ('zero', 0.0)], default='base', max_length=4, verbose_name='Tax rate'),
        ),
    ]