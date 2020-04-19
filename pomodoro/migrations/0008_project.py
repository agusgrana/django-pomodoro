# Generated by Django 2.2.9 on 2020-04-19 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pomodoro.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pomodoro', '0007_shares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('color', models.CharField(default=pomodoro.models.color, max_length=6)),
                ('url', models.URLField(blank=True, help_text='Optional link')),
                ('memo', models.TextField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.AddField(
            model_name='favorite',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pomodoro.Project'),
        ),
        migrations.AddField(
            model_name='pomodoro',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pomodoro.Project'),
        ),
    ]