from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Organization, User, Membership, Project
from .serializers import (
    OrganizationSerializer,
    UserSerializer,
    MembershipSerializer,
    ProjectSerializer,
)
from .permissions import IsOrganizationAdmin


class OrganizationListCreateView(ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def perform_create(self, serializer):
        organization = serializer.save()

        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role=Membership.Role.ADMIN,
        )

    def get_queryset(self):
        return Organization.objects.filter(membership__user=self.request.user)


class OrganizationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(membership__user=self.request.user)


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MembershipListCreateView(ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def get_queryset(self):
        return Membership.objects.filter(
            organization__membership__user=self.request.user
        )

    def perform_create(self, serializer):
        organization = serializer.validated_data["organization"]

        is_admin = Membership.objects.filter(
            user=self.request.user,
            organization=organization,
            role=Membership.Role.ADMIN,
        ).exists()

        if not is_admin:
            raise PermissionDenied(
                "You do not have permission to add members to this organization."
            )

        serializer.save()


class MembershipDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def get_queryset(self):
        return Membership.objects.filter(
            organization__membership__user=self.request.user
        )

    def perform_destroy(self, instance):
        if instance.role == Membership.Role.ADMIN:
            admin_count = Membership.objects.filter(
                organization=instance.organization, role=Membership.Role.ADMIN
            ).count()

            if admin_count == 1:
                raise PermissionDenied(
                    "Cannot delete the last admin of an organization."
                )

        instance.delete()


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(TokenObtainPairView):
    pass


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
