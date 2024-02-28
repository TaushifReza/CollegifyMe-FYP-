from django import forms

from post.models import Post


class PostForm(forms.ModelForm):
    custom_placeholders = {
        "post_content": "Post Content",
    }

    class Meta:
        model = Post
        fields = "post_content"

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            field_name = visible.name
            if field_name in self.custom_placeholders:
                visible.field.widget.attrs["placeholder"] = self.custom_placeholders[
                    field_name
                ]
