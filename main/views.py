from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.views.generic import UpdateView, DeleteView


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


def view(request):
    user = request.user
    tasks = user.task.all().order_by('-id')
    context = {'tasks': tasks}
    return render(request, 'main/view.html', context)


def data(request):
    tasks = Task.objects.order_by('-id')
    context = {'tasks': tasks}
    return render(request, 'main/data.html', context)


def create(request):
    error = ''
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            ttl = form.cleaned_data["title"]
            tsk = form.cleaned_data["task"]
            task = Task(title=ttl, task=tsk, user=request.user)
            task.save()
            request.user.task.add(task)
            return redirect('notes')
        else:
            error = 'Ошибка при добавлении'

    context = {'form': form, 'error': error}
    return render(request, 'main/create.html', context)


class TaskUpdateView(UpdateView):
    model = Task
    success_url = '/view'
    template_name = "main/create.html"

    form_class = TaskForm


class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/view'
    template_name = "main/delete.html"


def profile(request):
    context = {}
    return render(request, 'registration/profile.html', context)
