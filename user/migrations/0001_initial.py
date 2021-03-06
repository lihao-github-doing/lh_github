# Generated by Django 2.0.6 on 2020-11-05 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.IntegerField(blank=True, null=True)),
                ('salt', models.CharField(default='', max_length=50)),
            ],
            options={
                'db_table': 't_user',
            },
        ),
    ]
