# Generated by Django 4.2 on 2024-11-11 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='available_Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('slug', models.SlugField(max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'available_Courses',
                'verbose_name_plural': 'available Courses',
            },
        ),
        migrations.CreateModel(
            name='liveclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100, null=True)),
                ('class_description', models.TextField(max_length=1000, null=True, verbose_name='About the Live Class')),
                ('class_link', models.CharField(max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='studentattendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('student_email', models.EmailField(max_length=100, null=True, unique=True, verbose_name='Student Email')),
                ('Timeanddate', models.DateTimeField(auto_now=True, null=True, verbose_name='Time & date joined')),
            ],
            options={
                'verbose_name': 'studentattendance',
                'verbose_name_plural': 'Student Attendance',
            },
        ),
    ]