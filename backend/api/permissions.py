import traceback
from rest_framework import permissions


class IsAnnotatorOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow annotators to read and write their own annotations.
    """
    def has_object_permission(self, request, view, obj):

        # allow read permissions GET, HEAD or OPTIONS requests
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # always allow staff
        if request.user.is_staff:
            u = request.user
            print("Allowing staff {} : {}".format(u.pk, u.username))
            return True

        # allow only the owner of the annotation
        try:
            if obj and obj.annotator and request.user:
                return obj.annotator == request.user
        except:
            print("Failed to check object's annotator user. Denying request.")

        return False
