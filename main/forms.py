from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, Select

from .models import NoteActive, Topic, Color


class NoteForm(ModelForm):

    class Meta:
        model = NoteActive
        fields = ['title', 'text', 'topic', 'color']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Название"
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Запишите здесь свои мысли"
            })}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['topic'] = ModelChoiceField(
            queryset=Topic.objects.filter(user=user), required=False, empty_label="Выберите тему",
            widget=Select(attrs={
                'class': 'form-control',
                'placeholder': "Тема"
            })
        )
        self.fields['color'] = ModelChoiceField(
            queryset=Color.objects.all(), required=False, empty_label="Выберите цвет",
            widget=Select(attrs={
                'class': 'form-control',
                'placeholder': "Цвет"
            })
        )


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Название"
            })}
