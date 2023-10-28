from django import forms
from django.core.exceptions import ValidationError

from .models import Article, UserResponse


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = (
                  'title',
                  'text',
                  'category',
                  'image',
                  )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError('Заголовок и текст должны отличаться!')

        return cleaned_data


class ResponseForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '4',
    }))

    class Meta:
        model = UserResponse
        fields = ('article',
                  'text',)




