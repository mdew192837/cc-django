# Generated by Django 2.1.3 on 2018-11-20 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club_Classifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
