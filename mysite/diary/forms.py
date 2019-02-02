from django import forms
from .models import DiaryFile
from django.forms import ModelForm
import logging

logger = logging.getLogger('dairy.diary.forms')

class DiaryFileForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = DiaryFile
        fields = ['diary', 'file']
    def save(self, *args, **kwargs):
        # multiple file upload
        # NB: does not respect 'commit' kwarg
        file_list = self.files.getlist('file')
        logger.debug(file_list)

        self.instance.file = file_list[0]
        for file in file_list[1:]:
            DiaryFile.objects.create(
                diary=self.cleaned_data['diary'],
                file=file
            )

        return super().save(*args, **kwargs)
