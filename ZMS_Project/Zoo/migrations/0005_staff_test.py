# Generated by Django 2.1.1 on 2018-11-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zoo', '0004_auto_20181002_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='staff_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardid', models.CharField(db_column='cardID', max_length=10)),
            ],
            options={
                'db_table': 'staff_test',
                'managed': False,
            },
        ),
    ]
