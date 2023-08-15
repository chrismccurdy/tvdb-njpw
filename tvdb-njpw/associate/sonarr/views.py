from . import models, serializers
from .associate import Associator
from .sonarrytdl import get_recent_downloads
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AssociationViewSet(viewsets.ModelViewSet):
    queryset = models.Association.objects.all().order_by("-associated_at")
    serializer_class = serializers.AssociationSerializer

    @action(detail=False, url_path=r"recent(/?(?P<limit>\d+))?")
    def recent_associations(self, request, limit: int = 5):
        recent = Associator().get_recent_associations(int(limit))
        serialized = serializers.AssociationSerializer(recent, many=True).data
        return Response(serialized)


class NjpwWorldEpisodeViewSet(viewsets.ModelViewSet):
    queryset = models.NjpwWorldEpisode.objects.all().order_by("-air_date")
    serializer_class = serializers.NjpwWorldEpisodeSerializer

    @action(detail=False, url_path="unassociated")
    def unassociated_episodes(self, request):
        unassoc = Associator().get_unassociated_njpw_world_episodes()
        serialized = serializers.NjpwWorldEpisodeSerializer(unassoc, many=True).data
        return Response(serialized)

    @action(
        detail=False,
        url_path=r"downloads/recent(/?(?P<limit>\d+))?",
    )
    def recent_downloads(self, request, limit: int = 5):
        downloads = models.NjpwWorldEpisode.objects.order_by("-downloaded_at")[
            : int(limit)
        ]
        serialized = serializers.NjpwWorldEpisodeSerializer(downloads, many=True).data
        return Response(serialized)


class TvdbEpisodeViewSet(viewsets.ModelViewSet):
    queryset = models.TvdbEpisode.objects.all().order_by("-air_date")
    serializer_class = serializers.TvdbEpisodeSerializer

    @action(detail=False, url_path="unassociated")
    def unassociated_episodes(self, request):
        unassoc = Associator().get_unassociated_tvdb_episodes()
        serialized = serializers.TvdbEpisodeSerializer(unassoc, many=True).data
        return Response(serialized)

    @action(
        detail=False,
        url_path=r"downloads/recent(/?(?P<limit>\d+))?",
    )
    def recent_downloads(self, request, limit: int = 5):
        recent = get_recent_downloads(int(limit))
        serialized = serializers.TvdbEpisodeSerializer(recent, many=True).data
        return Response(serialized)


class TvdbSeriesViewSet(viewsets.ModelViewSet):
    queryset = models.TvdbSeries.objects.all()
    serializer_class = serializers.TvdbSeriesSerializer


class NjpwWorldSeriesViewSet(viewsets.ModelViewSet):
    queryset = models.NjpwWorldSeries.objects.all()
    serializer_class = serializers.NjpwWorldSeriesSerializer


def index(request):
    return HttpResponse("whatever")
