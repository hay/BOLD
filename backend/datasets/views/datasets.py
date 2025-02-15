import json
from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError

from datasets.models import Dataset
from datasets.serializers import DatasetSerializer
from datasets.services.search import TermPos
from datasets.tasks.pipeline import import_dataset, delete_dataset
from users.permissions import IsOwner


class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['mode', 'search_mode', 'state', 'id', 'creator']
    search_fields = ['name', 'source', 'description']

    def perform_create(self, serializer):
        if serializer.validated_data.get('mode') == Dataset.Mode.SPARQL.value and \
                serializer.validated_data.get('search_mode') == Dataset.SearchMode.LOCAL.value:
            raise ValidationError('Local search index for sparql datasets is not yet supported')

        if serializer.validated_data.get('search_mode', None) == Dataset.SearchMode.TRIPLYDB.value and \
                'tdb_id' not in serializer.validated_data.get('source', {}):
            raise ValidationError('TriplyDB dataset must be a TriplyDB dataset')

        if not settings.STARDOG_ENABLE and (
            serializer.validated_data.get('mode') != Dataset.Mode.SPARQL.value or
            serializer.validated_data.get('search_mode') == Dataset.SearchMode.LOCAL.value
        ):
            raise ValidationError('Local datasets are not enabled on this server')

        super().perform_create(serializer)

        instance: Dataset = serializer.instance
        instance.creator = self.request.user
        instance.save()

        instance.apply_async(
            import_dataset,
            (instance.id,),
            creator=self.request.user,
            name=f'Import dataset {instance.name}'
        )

    def perform_destroy(self, instance):
        instance.apply_async(
            delete_dataset,
            (instance.id,),
            creator=self.request.user,
            name=f'Deleting dataset {instance.name}'
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def get_permissions(self):
        permissions = super().get_permissions()

        if self.action in ['destroy']:
            permissions.append(IsOwner())

        return permissions


def parse_int_or_none(value: str) -> int:
    if value is None:
        return None
    return int(value)


@swagger_auto_schema(methods=['get'], manual_parameters=[
    openapi.Parameter('query', openapi.IN_QUERY, "Search query", type=openapi.TYPE_STRING),
    openapi.Parameter('pos', openapi.IN_QUERY, "Term Position", type=openapi.TYPE_STRING),
    openapi.Parameter('limit', openapi.IN_QUERY, "Limit", type=openapi.TYPE_INTEGER),
    openapi.Parameter('offset', openapi.IN_QUERY, "Offset", type=openapi.TYPE_INTEGER),
    openapi.Parameter('timeout', openapi.IN_QUERY, "Timeout", type=openapi.TYPE_INTEGER),
])
@api_view(['GET'])
def term_search(request: Request, id: UUID):
    dataset = Dataset.objects.get(id=id)

    q = request.GET.get('query', '')
    pos = TermPos(request.GET.get('pos', 'OBJECT'))
    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    timeout = int(request.GET.get('timeout', 5000))

    result = dataset.get_search_service().search(q, pos, limit, offset, timeout)
    return JsonResponse(result.to_dict())


@swagger_auto_schema(methods=['post'], manual_parameters=[
    openapi.Parameter('limit', openapi.IN_QUERY, "Limit", type=openapi.TYPE_INTEGER),
    openapi.Parameter('timeout', openapi.IN_QUERY, "Timeout", type=openapi.TYPE_INTEGER),
], request_body=openapi.Schema(
    type=openapi.TYPE_STRING,
    description='Query to be executed'
))
@api_view(['POST'])
def dataset_query(request: Request, id: UUID):
    dataset = Dataset.objects.get(id=id)

    limit = int(request.GET.get('limit', 10))
    timeout = int(request.GET.get('timeout', 5000))
    query = request.body.decode('utf-8')

    result = dataset.get_query_service().query(query, limit, timeout)
    return JsonResponse(result)
