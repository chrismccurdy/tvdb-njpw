"""
URL configuration for associate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
import sonarr.urls
from sonarr import views

router = routers.DefaultRouter()
router.register(r"associations", views.AssociationViewSet)
router.register(r"njpw_world_series", views.NjpwWorldSeriesViewSet)
router.register(r"njpw_world_episodes", views.NjpwWorldEpisodeViewSet)
router.register(r"tvdb_series", views.TvdbSeriesViewSet)
router.register(r"tvdb_episodes", views.TvdbEpisodeViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("sonarr/", include(sonarr.urls)),
    path("admin/", admin.site.urls),
]
