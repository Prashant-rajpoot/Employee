# Generated by Django 3.1.12 on 2022-01-13 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation_details', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Termination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('termination_letter', models.FileField(blank=True, upload_to='termination_letters')),
                ('clearance_form', models.FileField(blank=True, upload_to='termination_forms')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Offence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('resolved', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
                ('penalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.penalty')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField(unique=True)),
                ('type', models.CharField(max_length=40)),
                ('effective_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('status', models.CharField(default='Active', max_length=10)),
                ('risk', models.CharField(max_length=10)),
                ('document', models.FileField(upload_to='contracts')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.position')),
            ],
        ),
    ]
