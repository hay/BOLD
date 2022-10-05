# Generated by Django 4.1 on 2022-08-15 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tasks', '0002_alter_task_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
    ]