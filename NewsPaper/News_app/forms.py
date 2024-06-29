from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "author",
            "title",
            "text",
            "post_category",
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 30:
            raise ValidationError({
                "text": "Текст не может быть менее 30 символов."
            })

        return cleaned_data


