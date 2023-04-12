from .models import NoteActive, Topic
from django.forms import ModelForm, TextInput, Textarea


class NoteForm(ModelForm):
    class Meta:
        model = NoteActive
        fields = ['title', 'text']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Название"
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Запишите здесь свои мысли"
            })}


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Название"
            })}
