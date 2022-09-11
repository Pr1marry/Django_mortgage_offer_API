from django_filters import rest_framework as filters

from .models import Offer


class OfferFilterSet(filters.FilterSet):
    rate_min = filters.NumberFilter(field_name="rate_min", lookup_expr='gte')
    rate_max = filters.NumberFilter(field_name="rate_max", lookup_expr='lte')
    payment_min = filters.NumberFilter(field_name="payment_min", lookup_expr='gte')
    payment_max = filters.NumberFilter(field_name="payment_max", lookup_expr='lte')

    # def term_filter(self, queryset, name, value):
    #     return queryset.filter(term_min__gte=value, term_max__lte=value)

    class Meta:
        model = Offer
        fields = ['rate_min', 'rate_max', 'payment_min', 'payment_max']