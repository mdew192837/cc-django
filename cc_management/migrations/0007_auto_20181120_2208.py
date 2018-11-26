# Generated by Django 2.1.3 on 2018-11-21 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc_management', '0006_player_games_played'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='club_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc_management.Club', verbose_name='Club Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(default=0, verbose_name='# of Games Played'),
        ),
        migrations.AlterField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active?'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Club Rating'),
        ),
        migrations.AlterField(
            model_name='player',
            name='uscf_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='USCF ID'),
        ),
        migrations.AlterField(
            model_name='player',
            name='uscf_rating',
            field=models.IntegerField(blank=True, null=True, verbose_name='USCF Rating'),
        ),
    ]