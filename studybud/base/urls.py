from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home.index'),
    path('rooms/create/', views.rooms_create, name='rooms.create'),
    path('rooms/store/', views.rooms_store, name='rooms.store'),
    path('rooms/<str:pk>/edit', views.rooms_edit, name='rooms.edit'),
    path('rooms/<str:pk>/show', views.rooms_show, name='rooms.show'),
    path('rooms/<str:pk>/update', views.rooms_update, name='rooms.update'),
    path('rooms/<str:pk>/delete', views.rooms_delete, name='rooms.delete'),
]
