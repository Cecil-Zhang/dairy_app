# Generated by Django 2.1.4 on 2019-02-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_diaryfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='diary',
            name='weather',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
