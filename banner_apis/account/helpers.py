
from django.core.mail import send_mail
import random
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAdminUser
def send_otp_via_email(email):
    subject = 'Your account verification email'
    
    otp = random.randint(1000, 9999)
    message = f'Your otp is {otp}'
    
    email_from = settings.EMAIL_HOST

    send_mail(subject, message, email_from, [email ])
    
    return otp


        

class IsAuthenticatedOrCreate(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_admin == True:
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)
    
    
    
class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)

from rest_framework.pagination import PageNumberPagination
class Custom_Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        data={
        'next': self.get_next_link(),
        'previous': self.get_previous_link(),
        'results': data
        }
        return data