from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("associations/recent", views.recent_associations, name="recent_associations"),
    path(
        "associations/recent/<int:limit>",
        views.recent_associations,
        name="recent_associations",
    ),
    path(
        "njpw_world_episodes/unassociated",
        views.unassociated_njpw_world_episodes,
        name="unassociated_njpw_world_episodes",
    ),
    path(
        "tvdb_episodes/unassociated",
        views.unassociated_tvdb_episodes,
        name="unassociated_tvdb_episodes",
    ),
    path(
        "tvdb_episodes/downloads/recent",
        views.recent_downloads,
        name="recent_downloads",
    ),
    path(
        "tvdb_episodes/downloads/recent/<int:limit>",
        views.recent_downloads,
        name="recent_downloads",
    ),
]
