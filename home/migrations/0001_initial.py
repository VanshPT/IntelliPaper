# Generated by Django 5.1.1 on 2024-09-27 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('authors', models.CharField(max_length=1000)),
                ('abstract', models.TextField()),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
                ('extracted_text', models.TextField(blank=True)),
            ],
        ),
    ]
