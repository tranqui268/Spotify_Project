from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Cho phép tất cả request GET, HEAD, OPTIONS (đọc dữ liệu)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Chỉ cho phép chỉnh sửa/xóa nếu user là chủ playlist
        return obj.user == request.user