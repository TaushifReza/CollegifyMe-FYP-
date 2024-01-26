from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    custom_placeholders = {
        "email": "Enter your Email",
        "password": "Enter your Password",
        "confirm_password": "Confirm your Password",
    }

    class Meta:
        model = User
        fields = [
            "email",
        ]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not matched!!!")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control text-white"
            field_name = visible.name
            if field_name in self.custom_placeholders:
                visible.field.widget.attrs["placeholder"] = self.custom_placeholders[
                    field_name
                ]
