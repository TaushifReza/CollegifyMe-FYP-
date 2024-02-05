from django import forms

from college.models import CollegeProfile
from student.utils import allow_only_image_validator


class CollegeProfileForm(forms.ModelForm):
    college_logo = forms.FileField(validators=[allow_only_image_validator])

    custom_placeholders = {
        "college_name": "College Name",
        "college_logo": "College Logo",
        "website_url": "Website URL",
        "address": "Address",
        "phone_number": "Phone Number",
    }

    class Meta:
        model = CollegeProfile
        fields = [
            "college_name",
            "college_logo",
            "website_url",
            "address",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super(CollegeProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            field_name = visible.name
            if field_name in self.custom_placeholders:
                visible.field.widget.attrs["placeholder"] = self.custom_placeholders[
                    field_name
                ]
