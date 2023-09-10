from . import models, serializers
from .associate import Associator
from .sonarrytdl import (
    download,
    download_pending,
    get_download_status,
    get_recent_downloads,
)
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import threading


class AssociationViewSet(viewsets.ModelViewSet):
    queryset = models.Association.objects.all().order_by("-associated_at")
    serializer_class = serializers.AssociationSerializer

    @action(detail=False, url_path=r"recent(/?(?P<limit>\d+))?")
    def recent_associations(self, request, limit: int = 5):
        recent = Associator().get_recent_associations(int(limit))
        serialized = serializers.AssociationSerializer(recent, many=True).data
        return Response(serialized)

    @action(
        detail=False, methods=["POST"], url_path=r"download(/?(?P<association_id>\d+))?"
    )
    def download(self, request, association_id: int = None):
        response = {"downloading": True, "message": ""}
        if association_id is None:
            self.async_download_pending()
        else:
            association = models.Association.objects.filter(id=association_id)
            if association is not None:
                self.async_download(association)
            else:
                response.downloading = False
                response.message = "Association not found"
        return Response(response)

    def async_download(self, association):
        t = threading.Thread(target=download, args=association)
        t.setDaemon(True)
        t.start()

    def async_download_pending(self):
        t = threading.Thread(target=download_pending)
        t.setDaemon(True)
        t.start()

    @action(detail=False, methods=["GET"], url_path=r"download/status")
    def download_status(self, request):
        return Response(get_download_status())


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
