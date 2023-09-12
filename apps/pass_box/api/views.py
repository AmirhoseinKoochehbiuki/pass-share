from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from pass_box.models import *
from .serializers import *
from .permissions import *


class PassViewSet(ModelViewSet):
    """Pass CRUD in PassBox"""
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['target']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated &
                          (PassOwnerPermission_Create | PassOwnerPermission_Delete | PassOwnerPermission_Read | PassOwnerPermission_Update)]
    serializer_class = PassSerializer

    def get_queryset(self):
        return PassBox.objects.filter(owner_id=self.request.user.id)

    @action(detail=False)
    def shared_with_me(self, request):
        pass_codes_shared_id = [item['pass_code'] for item in ShareList.objects.filter(
            user=self.request.user.id).values('pass_code')]
        pass_codes = PassBox.objects.filter(id__in=pass_codes_shared_id)
        serializer = PassSerializer(pass_codes, many=True)
        return Response(serializer.data)


class ShareViewSet(ModelViewSet):
    """ShareList Management"""
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated &
                          (SharePassOwnerPermission_Create | SharePassOwnerPermission_Read | SharePassOwnerPermission_Update | SharePassOwnerPermission_Delete)]

    def get_serializer_class(self):
        if self.action == 'list':
            return ShareListSerializer
        return ShareSerializer

    def get_queryset(self):
        pass_codes_id = [item['id'] for item in PassBox.objects.filter(
            owner_id=self.request.user.id).values('id')]
        return ShareList.objects.filter(pass_code__in=pass_codes_id)
