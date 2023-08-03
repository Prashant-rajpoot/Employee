from django.contrib import admin
from .models import OvertimeApplication, OvertimePlan, OvertimeSchedule, TestCronJob

# Register your models here.

admin.site.register(OvertimeApplication)
admin.site.register(OvertimePlan)
admin.site.register(OvertimeSchedule)
admin.site.register(TestCronJob)
