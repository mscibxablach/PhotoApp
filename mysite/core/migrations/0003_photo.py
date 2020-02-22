# Generated by Django 2.1.3 on 2020-02-19 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_book_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='photos/pdfs/')),
                ('original', models.ImageField(blank=True, null=True, upload_to='photos/original/')),
            ],
        ),
    ]
