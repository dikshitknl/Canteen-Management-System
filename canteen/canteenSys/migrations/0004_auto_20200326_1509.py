# Generated by Django 3.0.4 on 2020-03-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteenSys', '0003_auto_20200326_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='menuImages/', verbose_name='Image of Item'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Available '),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Item Name '),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='options',
            field=models.SmallIntegerField(choices=[(1, 'Veg w egg'), (2, 'Veg w/o egg'), (3, 'Non-Veg')], default=2, verbose_name='Food Style (veg/non)'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='preparation_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Time required to prepare'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price (per Plate) '),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
