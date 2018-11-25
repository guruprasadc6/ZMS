# Generated by Django 2.1.1 on 2018-10-02 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zoo', '0003_auto_20181002_1905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authgroup',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authgrouppermissions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authpermission',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authuser',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='authusergroups',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangoadminlog',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangocontenttype',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangomigrations',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='djangosession',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='exhibit',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='livesin',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='looksafter',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='manages',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='ticketbookings',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='worksin',
            options={'managed': False},
        ),
    ]
