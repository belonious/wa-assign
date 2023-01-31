from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .movie_ordering import MovieOrdering
from .serializers import UserSerializer, MovieSerializer, OpinionSerializer
from ..models import Movie, Opinion

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class MovieViewSet(ReadOnlyModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filter_backends = (MovieOrdering,)
    permission_classes = (AllowAny,)

    @action(detail=True)
    def user_movies(self, request, pk=None):
        movies = Movie.objects.filter(submitted_by=pk)
        movies_json = MovieSerializer(movies, many=True, context={
            'request': request,
        })
        return Response(movies_json.data)


class OpinionViewSet(ReadOnlyModelViewSet):
    serializer_class = OpinionSerializer
    queryset = Opinion.objects.all()


@api_view(['POST', 'DELETE'])
def submit_opinion(request):

    if request.method == 'DELETE':
        user_id = request.user.id
        movie_id = request.data.get('movie_id')
        opinion = Opinion.objects.get(movie_id=movie_id, user_id=user_id)
        opinion.delete()
        return Response()

    if request.method == 'POST':
        user_id = request.user.id
        movie_id = request.data.get('movie_id')
        liked = request.data.get('liked')
        movie_submitted_by = Movie.objects.filter(submitted_by=user_id, id=movie_id)
        if movie_submitted_by:
            return Response("Can't add opinion since you submitted the movie", status=status.HTTP_406_NOT_ACCEPTABLE)
        opinion = Opinion(movie_id=movie_id, like=liked, user_id=user_id)
        opinion.save()
        return Response()
