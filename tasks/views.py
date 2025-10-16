from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from datetime import date


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        due_date_param = self.request.query_params.get('due_date')
        queryset = Task.objects.filter(owner=self.request.user)
        if status_param == 'completed':
            queryset = queryset.filter(status=True)
        elif status_param == 'pending':
            queryset = queryset.filter(status=False)
        if due_date_param == 'today':
            queryset = queryset.filter(due_date=date.today())
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status:
            return Response(
                {"error": "Completed tasks cannot be edited unless reverted to incomplete."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = not task.status
    task.save()
    return Response(TaskSerializer(task).data)
