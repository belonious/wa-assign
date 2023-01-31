from django.urls import path

from movierama_wa.users.api import views
from movierama_wa.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view, MovieSubmitView,
)

app_name = "users"
urlpatterns = [
    path("submit_opinion/", view=views.submit_opinion, name="submit_opinion"),
    path("submit_movie_f/", view=MovieSubmitView.as_view(), name="submit_movie_f"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
