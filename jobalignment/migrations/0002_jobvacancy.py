# Generated by Django 5.0.7 on 2024-09-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobalignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=200)),
            ],
        ),
    ]
