# Generated by Django 3.0.6 on 2020-06-21 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokerhand',
            old_name='big_blind',
            new_name='dealer',
        ),
        migrations.RenameField(
            model_name='pokerhand',
            old_name='small_blind',
            new_name='deck_size',
        ),
        migrations.RenameField(
            model_name='pokerroom',
            old_name='users',
            new_name='players',
        ),
        migrations.RemoveField(
            model_name='pokerhand',
            name='type',
        ),
        migrations.AddField(
            model_name='pokerroom',
            name='big_blind',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokerroom',
            name='small_blind',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokerroom',
            name='type',
            field=models.CharField(choices=[('TexasHoldEm', 'TexasHoldEm')], default='texas', max_length=50),
            preserve_default=False,
        ),
    ]
