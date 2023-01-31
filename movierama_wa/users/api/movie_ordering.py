from django.db.models import Count, Q
from rest_framework.filters import OrderingFilter


class MovieOrdering(OrderingFilter):
    allowed_custom_filters = ['hates', 'likes', 'dt']

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)

        if params and params in self.allowed_custom_filters:
            return params
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering == 'hates':
            return queryset \
                .annotate(opinion=Count('m_opinions', filter=Q(m_opinions__like=False))) \
                .order_by('-opinion')
        elif ordering == 'likes':
            return queryset \
                .annotate(opinion=Count('m_opinions', filter=Q(m_opinions__like=True))) \
                .order_by('-opinion')
        elif ordering == 'dt':
            return queryset.order_by('date_created')
        return queryset
