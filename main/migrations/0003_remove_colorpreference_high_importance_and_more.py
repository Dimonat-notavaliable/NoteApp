# Generated by Django 4.1.6 on 2023-05-18 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_color_colorpreference_user_preference'),
        ('main', '0002_alter_topic_options_alter_noteactive_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colorpreference',
            name='high_importance',
        ),
        migrations.RemoveField(
            model_name='colorpreference',
            name='low_importance',
        ),
        migrations.RemoveField(
            model_name='colorpreference',
            name='medium_importance',
        ),
        migrations.AlterField(
            model_name='noteactive',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note', to='register.color'),
        ),
        migrations.AlterField(
            model_name='noteinactive',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note_basket', to='register.color'),
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='ColorPreference',
        ),
    ]
