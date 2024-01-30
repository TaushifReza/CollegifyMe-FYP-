from django import forms

from student.models import StudentProfile
from student.utils import allow_only_image_validator


class StudentProfileForm(forms.ModelForm):
    profile_image = forms.FileField(validators=[allow_only_image_validator])
    cover_image = forms.FileField(validators=[allow_only_image_validator])

    custom_placeholders = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "profile_image": "Profile Image",
        "cover_image": "Cover Image",
        "current_address": "Current Address",
        "permanent_address": "Permanent Address",
    }

    class Meta:
        model = StudentProfile
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "cover_image",
            "current_address",
            "permanent_address",
        ]

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            field_name = visible.name
            if field_name in self.custom_placeholders:
                visible.field.widget.attrs["placeholder"] = self.custom_placeholders[
                    field_name
                ]
