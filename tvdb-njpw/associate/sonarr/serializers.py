from . import models
from rest_framework import serializers


class NjpwWorldSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NjpwWorldSeries
        fields = "__all__"


class NjpwWorldEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NjpwWorldEpisode
        fields = "__all__"


class TvdbSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TvdbSeries
        fields = "__all__"


class TvdbEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TvdbEpisode
        fields = "__all__"


class AssociationSerializer(serializers.ModelSerializer):
    tvdb_episode = TvdbEpisodeSerializer(read_only=True)
    njpw_world_episode = NjpwWorldEpisodeSerializer(read_only=True)

    class Meta:
        model = models.Association
        fields = "__all__"
