from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('data', views.data, name='data'),
    path('create_note', views.create_note, name='create_note'),
    path('create_topic', views.create_topic, name='create_topic'),
    path('view', views.view, name='notes'),
    path('view/topic/<int:pk>', views.view_topic, name='topic_notes'),
    path('basket', views.basket, name='basket'),
    path('profile', views.profile, name='profile'),
    path('task/<int:pk>/update', views.NoteUpdateView.as_view(), name='note-upd'),
    path('task/<int:pk>/delete', views.delete_note, name='note-dlt'),
    path('task/<int:pk>/download/<str:extension>', views.download_note, name='note-dwnld'),
    path('task/<int:pk>/retrieve', views.retrieve_note, name='note-rtr'),
]

urlpatterns += staticfiles_urlpatterns()
