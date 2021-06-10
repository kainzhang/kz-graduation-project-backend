from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, filters, permissions


# Create your views here.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff']
        extra_kwargs = {
            'username': {
                'min_length': 6,
                'max_length': 16
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20
            }
        }


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id']
    ordering = ['id']
    search_fields = ['=username']
