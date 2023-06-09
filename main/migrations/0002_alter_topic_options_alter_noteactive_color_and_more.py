# Generated by Django 4.1.6 on 2023-05-18 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={},
        ),
        migrations.AlterField(
            model_name='noteactive',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note', to='main.color'),
        ),
        migrations.AlterField(
            model_name='noteactive',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note', to='main.topic'),
        ),
        migrations.AlterField(
            model_name='noteinactive',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note_basket', to='main.color'),
        ),
        migrations.CreateModel(
            name='ColorPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('high_importance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='high', to='main.color')),
                ('low_importance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='low', to='main.color')),
                ('medium_importance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medium', to='main.color')),
            ],
        ),
    ]
