from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    task = Task.objects.get(pk=pk, owner=request.user)
    task.status = not task.status 
    task.save()
    return Response(TaskSerializer(task).data)