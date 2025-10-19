from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from datetime import date, datetime


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        due_date_param = self.request.query_params.get('due_date')
        queryset = Task.objects.filter(owner=self.request.user)

        if status_param == 'completed':
            queryset = queryset.filter(status=Task.STATUS_COMPLETED)
        elif status_param == 'pending':
            queryset = queryset.filter(status=Task.STATUS_PENDING)

        if due_date_param:
            if due_date_param == 'today':
                queryset = queryset.filter(due_date=date.today())
            else:
                try:
                    parsed_date = datetime.strptime(due_date_param, "%Y-%m-%d").date()
                    queryset = queryset.filter(due_date=parsed_date)
                except ValueError:
                    pass 

        return queryset  
    
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date, datetime
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        due_date_param = self.request.query_params.get('due_date')
        queryset = Task.objects.filter(owner=self.request.user)

       
        if status_param == 'completed':
            queryset = queryset.filter(status=Task.STATUS_COMPLETED)
        elif status_param == 'pending':
            queryset = queryset.filter(status=Task.STATUS_PENDING)

          
        if due_date_param:
            if due_date_param == 'today':
                queryset = queryset.filter(due_date=date.today())
            else:
                try:
                    parsed_date = datetime.strptime(due_date_param, "%Y-%m-%d").date()
                    queryset = queryset.filter(due_date=parsed_date)
                except ValueError:
                    pass

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        status_param = request.query_params.get('status')
        due_date_param = request.query_params.get('due_date')

        if not queryset.exists():
            if status_param == 'pending':
                return Response({"message": "No pending tasks available."}, status=status.HTTP_200_OK)
            elif status_param == 'completed':
                return Response({"message": "No completed tasks available."}, status=status.HTTP_200_OK)
            elif due_date_param:
                return Response({"message": "No tasks found for the selected date."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No tasks found."}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status == Task.STATUS_COMPLETED:
            return Response(
                {"error": "Completed tasks cannot be edited unless reverted to pending."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
  
    task.status = (
        Task.STATUS_COMPLETED
        if task.status == Task.STATUS_PENDING
        else Task.STATUS_PENDING
    )
    task.save()
    return Response(TaskSerializer(task).data)
