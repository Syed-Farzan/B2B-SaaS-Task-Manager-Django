from django.urls import path

from .views import (
    OrganizationListCreateView,
    OrganizationDetailView,
    UserListCreateView,
    UserDetailView,
    MembershipDetailView,
    MembershipListCreateView,
    UserRegistrationView,
    UserLoginView,
    UserMeView,
    ProjectListCreateView,
    ProjectDetailView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="user-me"),
    path(
        "organizations/",
        OrganizationListCreateView.as_view(),
        name="organization-list",
    ),
    path(
        "organizations/<uuid:pk>/",
        OrganizationDetailView.as_view(),
        name="organization-detail",
    ),
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "memberships/",
        MembershipListCreateView.as_view(),
        name="membership-list",
    ),
    path(
        "memberships/<int:pk>/",
        MembershipDetailView.as_view(),
        name="membership-detail",
    ),
    path("projects/", ProjectListCreateView.as_view(), name="project-list"),
    path(
        "projects/<uuid:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
]
