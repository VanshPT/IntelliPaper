# Generated by Django 3.2 on 2024-10-23 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_vectordocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citations', models.TextField()),
                ('paper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.researchpaper')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]