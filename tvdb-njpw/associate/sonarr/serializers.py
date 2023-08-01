from .models import Association, NjpwWorldEpisode, TvdbEpisode
from rest_framework import serializers


class NjpwWorldEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NjpwWorldEpisode
        fields = '__all__'

class TvdbEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvdbEpisode
        fields = '__all__'

class AssociationSerializer(serializers.ModelSerializer):
    tvdb_episode = TvdbEpisodeSerializer(read_only=True)
    njpw_world_episode = NjpwWorldEpisodeSerializer(read_only=True)

    class Meta:
        model = Association
        fields = '__all__'
