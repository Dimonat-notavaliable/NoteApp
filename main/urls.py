from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('data', views.data, name='data'),
    path('create', views.create, name='create'),
    path('view', views.view, name='notes'),
    path('profile', views.profile, name='profile'),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name='task-upd'),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-dlt'),
]

urlpatterns += staticfiles_urlpatterns()