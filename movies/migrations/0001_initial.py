# Generated by Django 2.1 on 2020-07-23 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('release_date', models.DateTimeField()),
                ('run_time', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
