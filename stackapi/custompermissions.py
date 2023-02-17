from rest_framework import permissions

class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.user==obj.user)
        return request.user==obj.user




# safe-method--list,get,detail
# unsafe-method put,patch,delete1``
        