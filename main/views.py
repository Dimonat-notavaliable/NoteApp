from django.shortcuts import render, redirect
from .models import Note, Topic
from .forms import NoteForm, TopicForm
from django.views.generic import UpdateView, DeleteView


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


def view(request):
    user = request.user
    notes = user.note.all().order_by('-id')
    topics = user.topic.all().order_by('-id')
    context = {'notes': notes, 'topics': topics}
    return render(request, 'main/view.html', context)


def data(request):
    notes = Note.objects.order_by('-id')
    context = {'notes': notes}
    return render(request, 'main/data.html', context)


def create_note(request):
    error = ''
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            ttl = form.cleaned_data["title"]
            txt = form.cleaned_data["text"]
            note = Note(title=ttl, text=txt, user=request.user)
            note.save()
            request.user.note.add(note)
            return redirect('notes')
        else:
            error = 'Ошибка при добавлении'

    context = {'form': form, 'error': error}
    return render(request, 'main/create_note.html', context)


def create_topic(request):
    error = ''
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            ttl = form.cleaned_data["title"]
            topic = Topic(title=ttl, user=request.user)
            topic.save()
            request.user.topic.add(topic)
            return redirect('notes')
        else:
            error = 'Ошибка при добавлении'

    context = {'form': form, 'error': error}
    return render(request, 'main/create_topic.html', context)


class TaskUpdateView(UpdateView):
    model = Note
    success_url = '/view'
    template_name = "main/create_note.html"

    form_class = NoteForm


class TaskDeleteView(DeleteView):
    model = Note
    success_url = '/view'
    template_name = "main/delete.html"


def profile(request):
    context = {}
    return render(request, 'registration/profile.html', context)
