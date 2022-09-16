from django_filters import filters, FilterSet
from reviews.models import Titles


class TitleFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ['name', 'category', 'genre', 'year']
