from . import models
from collections import OrderedDict
from rest_framework import serializers


class NjpwWorldSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NjpwWorldSeries
        fields = "__all__"


class NjpwWorldEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NjpwWorldEpisode
        fields = "__all__"


class NjpwWorldEpisodeField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(NjpwWorldEpisodeField, self).to_representation(value)
        try:
            item = models.NjpwWorldEpisode.objects.get(pk=pk)
            serializer = NjpwWorldEpisodeSerializer(item)
            return serializer.data
        except models.NjpwWorldEpisode.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([item.id, str(item)] for item in queryset)


class TvdbSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TvdbSeries
        fields = "__all__"


class TvdbEpisodeField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(TvdbEpisodeField, self).to_representation(value)
        try:
            item = models.TvdbEpisode.objects.get(pk=pk)
            serializer = TvdbEpisodeSerializer(item)
            return serializer.data
        except models.TvdbEpisode.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([item.id, str(item)] for item in queryset)


class TvdbEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TvdbEpisode
        fields = "__all__"


class AssociationSerializer(serializers.ModelSerializer):
    tvdb_episode = TvdbEpisodeField(queryset=models.TvdbEpisode.objects.all())
    njpw_world_episode = NjpwWorldEpisodeField(
        queryset=models.NjpwWorldEpisode.objects.all()
    )

    class Meta:
        model = models.Association
        fields = "__all__"

    def create(self, validated_data):
        return models.Association.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.tvdb_episode = validated_data.get(
            "tvdb_episode", instance.tvdb_episode
        )
        instance.njpw_world_episode = validated_data.get(
            "njpw_world_episode", instance.njpw_world_episode
        )
        instance.save()
        return instance
