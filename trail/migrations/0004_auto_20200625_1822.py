# Generated by Django 3.0.7 on 2020-06-25 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trail', '0003_auto_20200625_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
