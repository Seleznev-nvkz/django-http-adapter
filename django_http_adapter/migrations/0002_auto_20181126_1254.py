# Generated by Django 2.0 on 2018-11-26 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_http_adapter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTTPRetryData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('exception_info', models.TextField()),
                ('app_id', models.IntegerField()),
                ('data', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Retry Data',
            },
        ),
        migrations.AlterModelOptions(
            name='httpretry',
            options={'verbose_name_plural': 'Retry'},
        ),
        migrations.AlterUniqueTogether(
            name='httpretrydata',
            unique_together={('data', 'app_id')},
        ),
    ]
