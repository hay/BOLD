# Generated by Django 4.0.6 on 2022-07-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0006_rename_database_dataset_local_database_dataset_mode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='mode',
            field=models.CharField(choices=[('LOCAL', 'Imported locally '), ('SPARQL', 'From SPARQL endpoint')], default='LOCAL', max_length=255),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='search_mode',
            field=models.CharField(choices=[('LOCAL', 'Imported locally '), ('WIKIDATA', 'From Wikidata')], default='LOCAL', max_length=255),
        ),
    ]