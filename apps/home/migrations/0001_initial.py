# Generated by Django 3.2.6 on 2025-01-02 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('program', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.CharField(blank=True, max_length=100, null=True)),
                ('difficulty', models.CharField(blank=True, max_length=50, null=True)),
                ('servings', models.CharField(blank=True, max_length=50, null=True)),
                ('ingredients', models.TextField()),
                ('steps', models.TextField()),
                ('tags', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='home.author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='home.category')),
            ],
        ),
    ]
