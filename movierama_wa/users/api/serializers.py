from django.contrib.auth import get_user_model
from rest_framework import serializers
from collections import Counter
from movierama_wa.users.models import Movie, Opinion

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail"}
        }


class UserOpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = ["username", "name", "url", "id"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail"}
        }


class OpinionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Opinion
        depth = 1
        fields = ['like', 'user']


class MovieSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer()
    opinions = OpinionSerializer(source='m_opinions', many=True)
    aggr_opinions = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        depth = 1
        fields = ["title", "description", "date_created", "submitted_by", "opinions",
                  "aggr_opinions", "id"]

    def get_aggr_opinions(self, obj):
        movie_opinions = obj.m_opinions.values()
        res = {}
        opinion_stats = dict(Counter(movie_opinion['like'] for movie_opinion in movie_opinions))
        res['opinions'] = {
            'likes': opinion_stats.get(True, 0),
            'hates': opinion_stats.get(False, 0)
        }
        user = self.context['request'].user
        if user:
            user_opinion = list(
                filter(lambda opinion: opinion['user_id'] == user.id, movie_opinions))
            if not user_opinion:
                res['liked'] = None
            else:
                res['liked'] = {'value': user_opinion[0]['like'], 'id': user_opinion[0]['id']}

        return res
