# Generated by Django 3.2.14 on 2022-07-31 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatiskIncidents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_avtor_file', models.CharField(max_length=150)),
                ('id_avtor_file', models.IntegerField()),
                ('name_file', models.CharField(max_length=150)),
                ('date_file', models.DateField()),
                ('gp_all', models.IntegerField()),
                ('gp_unical', models.IntegerField()),
                ('ip_all', models.IntegerField()),
                ('ip_unical', models.IntegerField()),
                ('MAC_all', models.IntegerField()),
                ('MAC_unical', models.IntegerField()),
                ('PROBLEM_all', models.IntegerField()),
                ('PROBLEM_unical', models.IntegerField()),
            ],
        ),
    ]
