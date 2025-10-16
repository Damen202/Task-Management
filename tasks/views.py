from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404



class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        due_date = self.request.query_params.get('due_date')
        queryset = Task.objects.filter(owner=self.request.user)
        if status == 'completed':
            queryset = queryset.filter(status=True)
        elif status == 'pending':
            queryset = queryset.filter(status=False)
        if due_date == 'today':
            from datetime import date
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
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optional: return only tasks owned by the current user
        return self.queryset.filter(owner=self.request.user)

    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    task.status = not task.status
    task.save()
    return Response(TaskSerializer(task).data)
