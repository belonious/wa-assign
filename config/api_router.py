from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from movierama_wa.users.api.views import UserViewSet, MovieViewSet, OpinionViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("movies", MovieViewSet)
router.register("opinions", OpinionViewSet)


app_name = "api"
urlpatterns = router.urls
