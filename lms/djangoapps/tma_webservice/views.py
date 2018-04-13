"""
Student API Views
"""

from .serializers import StudentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


from openedx.core.lib.api.view_utils import view_auth_classes, DeveloperErrorViewMixin

@view_auth_classes(is_authenticated=True)
class StudentInfo(APIView):
    def get_object(self, email):
        try :
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, email, format=None):
        student = self.get_object(email)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
