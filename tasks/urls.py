from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, complete_task, CategoryListCreateView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('<int:id>/complete/', complete_task, name='complete-task'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
]
