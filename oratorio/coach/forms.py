from django import forms
from coach.models import Document

import os
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
    def clean_document(self):
        file = self.cleaned_data.get('document')
        if file:
            if file._size > 20*1024*1024:
                 raise ValidationError("Audio file too large ( > 20mb )")
            # if not file.content-type in ["audio/wav"]:
            #     raise ValidationError("Content-Type is not wav")
            if not os.path.splitext(file.name)[1] in [".wav"]:
                 raise ValidationError("Doesn't have proper extension")
            # Here we need to now to read the file and see if it's actually              # a valid audio file. I don't know what the best library is to
            # to do this
            # if not some_lib.is_audio(file.content):
            #     raise ValidationError("Not a valid audio file")
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")
