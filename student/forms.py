from django import forms

from student.models import StudentProfile, StudentEducation
from student.utils import allow_only_image_validator


class StudentProfileForm(forms.ModelForm):
    profile_image = forms.FileField(
        validators=[allow_only_image_validator], required=False
    )
    cover_image = forms.FileField(
        validators=[allow_only_image_validator], required=False
    )

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


class StudentEducationForm(forms.ModelForm):
    custom_placeholders = {
        "level_of_education": "Level of Education",
        "degree_name": "Degree Name",
        "college_name": "College Name",
        "start_date": "Start Date",
        "end_date": "End Date",
    }

    class Meta:
        model = StudentEducation
        fields = [
            "level_of_education",
            "degree_name",
            "college_name",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentEducationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            field_name = visible.name
            if field_name in self.custom_placeholders:
                visible.field.widget.attrs["placeholder"] = self.custom_placeholders[
                    field_name
                ]
