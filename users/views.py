from django.contrib.auth.models import User
from rest_framework import viewsets, filters

from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    ordering = ['id']
    search_fields = ['=username']
