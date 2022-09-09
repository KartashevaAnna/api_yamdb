from rest_framework import permissions

#
#
# class AuthorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )
#
    # def has_object_permission(self, request, view, obj):
    #     return (
    #         request.method in permissions.SAFE_METHODS
    #         or obj.author == request.user
    #     )


class AnonymousReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class NotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role != 'moderator'
        )



# class NotAuthorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )
#
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or obj.author != request.user
#         )
