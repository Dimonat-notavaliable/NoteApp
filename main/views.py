from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.utils.timezone import utc

from .models import NoteActive, Topic, NoteInactive
from .forms import NoteForm, TopicForm
from django.views.generic import UpdateView, DeleteView


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


def profile(request):
    context = {}
    return render(request, 'registration/profile.html', context)


def view(request):
    user = request.user
    notes = user.note.all().filter(topic__isnull=True).order_by('-id')
    topics = user.topic.all().order_by('-id')
    context = {'notes': notes, 'topics': topics}
    return render(request, 'main/view.html', context)


def basket(request):
    user = request.user
    user.note_basket.filter(date_deleted__lte=datetime.utcnow().replace(tzinfo=utc) - timedelta(hours=1)).delete()
    notes = user.note_basket.all().order_by('-date_deleted')
    context = {'notes': notes}
    return render(request, 'main/basket.html', context)


def data(request):
    notes = NoteActive.objects.order_by('-id')
    context = {'notes': notes}
    return render(request, 'main/data.html', context)


def create_note(request):
    error = ''
    form = NoteForm(user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            ttl = form.cleaned_data["title"]
            txt = form.cleaned_data["text"]
            topic = form.cleaned_data["topic"]
            color = form.cleaned_data["color"]
            note = NoteActive(title=ttl, text=txt, user=request.user, topic=topic, color=color)
            note.save()
            request.user.note.add(note)
            return redirect('notes')
        else:
            error = form.errors

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


class NoteUpdateView(UpdateView):
    model = NoteActive
    success_url = '/view'
    template_name = "main/create_note.html"


def delete_note(request, pk):
    if request.method == 'POST':
        note = NoteActive.objects.get(id=pk)
        note.place_in_basket()
        return redirect('notes')


def retrieve_note(request, pk):
    if request.method == 'POST':
        note = NoteInactive.objects.get(id=pk)
        note.retrieve()
        return redirect('basket')
