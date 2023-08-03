from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from leave.models import LeaveRecord


class LeaveRecordForm(ModelForm):
    class Meta:
        model = LeaveRecord
        exclude = ("employee", "leave_year")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()


