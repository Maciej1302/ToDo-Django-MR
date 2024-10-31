from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Case, Task
from .serializers import CaseSerializer, TaskSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


"""Generic classed base view for creating and listing cases and tasks"""


class CaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = [IsAuthenticated]


"""Generic classed base view for retrieving, updating and destroying cases"""


class CaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
