# Generated by Django 4.0.8 on 2023-03-23 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informations', '0002_accounting'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounting',
            name='obligor',
            field=models.CharField(choices=[('owner', '임대인'), ('concierge', '관리단')], default='owner', max_length=10),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='kind',
            field=models.CharField(choices=[('deposit', '입금'), ('withdrawal', '출금')], max_length=12),
        ),
    ]
