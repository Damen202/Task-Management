from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, complete_task



urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('<int:pk>/complete/', complete_task, name='complete-task'),
]
