# Generated by Django 2.1.5 on 2019-01-25 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='shipment_accepted',
            field=models.ForeignKey(db_column='shipment', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Shipment'),
        ),
    ]
