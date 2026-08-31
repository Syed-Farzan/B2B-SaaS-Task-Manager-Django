from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from users.models import Membership
from users.permissions import IsOrganizationAdmin


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            project__organization__membership__user=self.request.user
        )

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        organization = project.organization
        is_admin = Membership.objects.filter(
            user=self.request.user,
            organization=organization,
            role=Membership.Role.ADMIN,
        ).exists()

        if not is_admin:
            raise PermissionDenied(
                "You do not have permission to create tasks in this organization."
            )

        serializer.save()


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def get_queryset(self):
        return Task.objects.filter(
            project__organization__membership__user=self.request.user
        )
