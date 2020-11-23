from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instruction/', views.instruction, name='instruction'),
    path('upload/', views.upload, name='upload'),
    path('analysis/', views.analysis, name='analysis'),
    path('authors/', views.authors, name='authors'),
]
