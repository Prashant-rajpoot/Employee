from crispy_forms.helper import FormHelper
from django import forms

from payroll.models import CSV


class CSVForm(forms.ModelForm):
    class Meta:
        model = CSV
        fields = ("file_name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
