from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, complete_task, CategoryListCreateView
from . import views

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('<int:id>/complete/', complete_task, name='complete-task'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
]
