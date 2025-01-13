from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget

from profitpages.models import Content


class PublicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autofocus": ""})

        self.fields['content'].widget = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name="extends"
        )
        self.fields["content"].required = False

    class Meta:
        model = Content
        fields = ("title", "description", "preview", "content", "publisher")