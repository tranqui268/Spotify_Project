from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission check for Admin.
    Cho phép chỉ admin được phép truy cập API này.
    """

    def has_permission(self, request, view):
        # Kiểm tra xem người dùng có phải là admin hay không
        return request.user and request.user.is_staff