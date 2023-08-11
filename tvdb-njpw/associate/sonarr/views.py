from . import models, serializers
from .associate import Associator
from .logging import logger
from .sonarrytdl import get_recent_downloads
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


class AssociationViewSet(viewsets.ModelViewSet):
    queryset = models.Association.objects.all().order_by("-associated_at")
    serializer_class = serializers.AssociationSerializer


class NjpwWorldEpisodeViewSet(viewsets.ModelViewSet):
    queryset = models.NjpwWorldEpisode.objects.all().order_by("-air_date")
    serializer_class = serializers.NjpwWorldEpisodeSerializer


class TvdbEpisodeViewSet(viewsets.ModelViewSet):
    queryset = models.TvdbEpisode.objects.all().order_by("-air_date")
    serializer_class = serializers.TvdbEpisodeSerializer


class TvdbSeriesViewSet(viewsets.ModelViewSet):
    queryset = models.TvdbSeries.objects.all()
    serializer_class = serializers.TvdbSeriesSerializer


class NjpwWorldSeriesViewSet(viewsets.ModelViewSet):
    queryset = models.NjpwWorldSeries.objects.all()
    serializer_class = serializers.NjpwWorldSeriesSerializer


def index(request):
    return HttpResponse("whatever")


@api_view(["GET"])
def recent_associations(request, limit: int = 5):
    recent = Associator().get_recent_associations(limit)
    serialized = serializers.AssociationSerializer(recent, many=True).data
    return Response(serialized)


@api_view(["GET"])
def unassociated_tvdb_episodes(request):
    unassoc = Associator().get_unassociated_tvdb_episodes()
    serialized = serializers.TvdbEpisodeSerializer(unassoc, many=True).data
    return Response(serialized)


@api_view(["GET"])
def unassociated_njpw_world_episodes(request):
    unassoc = Associator().get_unassociated_njpw_world_episodes()
    serialized = serializers.NjpwWorldEpisodeSerializer(unassoc, many=True).data
    return Response(serialized)


@api_view(["GET"])
def recent_downloads(request, limit: int = 5):
    recent = get_recent_downloads(limit)
    serialized = serializers.TvdbEpisodeSerializer(recent, many=True).data
    return Response(serialized)
