from rest_framework.permissions import BasePermission


# Define role constants
ROLE_ADMIN = 'admin'  # Администратор
ROLE_CUSTOMER = 'customer'  # Заказчик
ROLE_CONTRACTOR = 'contractors'  # Подрядчики
ROLE_USER = 'user' # Пользователь
    

class IsAdmin(BasePermission):
    """Rights only for author"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='admin').exists())
    

class IsCustomer(BasePermission):
    """Rights only for customer"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.groups.filter(name='customer').exists())


class IsContractors(BasePermission):
    """Rights only for contractors"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='contractors').exists()


class IsUser(BasePermission):
    """Rights only for user"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='user').exists()


class IsLogin(BasePermission):
    """Rights only for Login"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated)
