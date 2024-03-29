# Generated by Django 4.0.8 on 2023-03-01 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherFcst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fcstDate', models.CharField(max_length=8)),
                ('fcstTime', models.CharField(max_length=4)),
                ('LGT', models.CharField(blank=True, max_length=10, null=True)),
                ('PTY', models.CharField(blank=True, max_length=10, null=True)),
                ('RN1', models.CharField(blank=True, max_length=10, null=True)),
                ('SKY', models.CharField(blank=True, max_length=10, null=True)),
                ('T1H', models.CharField(blank=True, max_length=10, null=True)),
                ('REH', models.CharField(blank=True, max_length=10, null=True)),
                ('UUU', models.CharField(blank=True, max_length=10, null=True)),
                ('VVV', models.CharField(blank=True, max_length=10, null=True)),
                ('VEC', models.CharField(blank=True, max_length=10, null=True)),
                ('WSD', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': '날씨',
                'verbose_name_plural': '날씨 api',
            },
        ),
    ]
