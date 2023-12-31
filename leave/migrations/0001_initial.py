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
            name='Leave_Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(max_length=45)),
                ('leave_days', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LeavePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('plan_date', models.DateField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('expired', models.BooleanField(default=False)),
                ('approval_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Expired', 'Expired')], default='Pending', max_length=8)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_date', models.DateField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('no_of_days', models.IntegerField(default=1)),
                ('supervisor_status', models.CharField(default='Pending', max_length=15)),
                ('supervisor_comment', models.TextField(blank=True, default='None', null=True)),
                ('hod_status', models.CharField(default='Pending', max_length=15)),
                ('hod_comment', models.TextField(blank=True, default='None', null=True)),
                ('hr_status', models.CharField(default='Pending', max_length=15)),
                ('hr_comment', models.TextField(blank=True, default='None', null=True)),
                ('overall_status', models.CharField(default='Pending', max_length=10)),
                ('remarks', models.TextField(default='None')),
                ('balance', models.IntegerField(default=0)),
                ('expired', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.department')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Employees', to='employees.employee')),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hod', to='employees.employee')),
                ('hr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hr', to='employees.employee')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.leave_types')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Supervisor', to='employees.employee')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.team')),
            ],
        ),
        migrations.CreateModel(
            name='annual_planner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_year', models.CharField(max_length=5)),
                ('leave_month', models.CharField(default='Jan', max_length=4)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('no_of_days', models.IntegerField(default=0)),
                ('status', models.CharField(default='Pending', max_length=15)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
                ('leave', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leave.leave_types')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_year', models.IntegerField()),
                ('entitlement', models.IntegerField(default=21)),
                ('residue', models.IntegerField(default=0)),
                ('leave_applied', models.IntegerField(default=0)),
                ('total_taken', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
            options={
                'unique_together': {('employee', 'leave_year')},
            },
        ),
    ]
