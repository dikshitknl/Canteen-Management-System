# Generated by Django 3.0.4 on 2020-03-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteenSys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='empNum',
            field=models.CharField(default=1, max_length=6, verbose_name='Employee ID '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, '--Select--'), (1, 'Male'), (2, 'Female'), (3, 'Others')], default=0, verbose_name='Gender '),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='options',
            field=models.SmallIntegerField(choices=[(1, 'Veg w egg'), (2, 'Veg w/o egg'), (3, 'Non-Veg')], default=2),
        ),
        migrations.AlterField(
            model_name='person',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Position '),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name '),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(max_length=15, unique=True, verbose_name='Phone # '),
        ),
    ]
