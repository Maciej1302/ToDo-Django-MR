from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Case, Task
from .serializers import CaseSerializer, TaskSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    View to list all tasks or create a new task item.

    - `GET`: Returns a list of all tasks.
    - `POST`: Creates a new task item.
    """

    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """
        Handles saving tasks for given user.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Handles filtering tasks for given user.
        """
        return Task.objects.filter(user=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, destroy task item.

    - `GET`: Returns a single task item.
    - `DELETE`: Destroy a single task item.
    - `UPDATE`: UPDATE a single task item.
    """

    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Handles filtering task for given user.
        """
        return Task.objects.filter(user=self.request.user)


class CaseListCreateAPIView(generics.ListCreateAPIView):
    """
     View to list all tasks or create a new case item.

    - `GET`: Returns a list of all cases.
    - `POST`: Creates a new case item.
    """

    serializer_class = CaseSerializer

    def perform_create(self, serializer):
        """
        Handles saving case for given user.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Handles filtering case for given user.
        """
        return Case.objects.filter(user=self.request.user)


class CaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, destroy case item.

    - `GET`: Returns a single case item.
    - `DELETE`: Destroy a single case item.
    - `UPDATE`: UPDATE a single case item.
    """

    serializer_class = CaseSerializer

    def get_queryset(self):
        """
        Handles filtering case for given user.
        """
        return Case.objects.filter(user=self.request.user)
