from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizationAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "organization"):
            organization = obj.organization

        else:
            organization = obj.project.organization

        return organization.membership_set.filter(
            user=request.user,
            role="admin",
        ).exists()
