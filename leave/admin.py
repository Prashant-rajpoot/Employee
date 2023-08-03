from django.contrib import admin

# Register your models here.
from .models import Leave_Types, LeaveApplication, LeaveRecord, LeavePlan

admin.site.register(Leave_Types)
admin.site.register(LeaveApplication)
admin.site.register(LeaveRecord)
admin.site.register(LeavePlan)