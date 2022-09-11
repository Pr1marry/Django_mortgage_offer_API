from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .filters import OfferFilterSet
from .models import Offer
from .serializers import OfferSerializer


def get_payment(rate, price, deposit, year):
    m_rate = (rate / 12.0 / 100)
    o_rate = (1 + m_rate) ** (year * 12)
    total = price - float(price * float(deposit / 100.0))
    payment = (total * m_rate * o_rate / (o_rate - 1))
    return payment


class OfferApiViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    ordering_fields = ['rate_min', 'rate_max', 'payment_min', 'payment_max']
    filterset_class = OfferFilterSet

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get('order') == 'rate':
            queryset = sorted(queryset, key=lambda x: x.rate_min)
        if request.GET.get('order') == '-rate':
            queryset = sorted(queryset, key=lambda x: -x.rate_min)
        term = request.GET.get('term')
        if term:
            term = float(term)
            queryset = [offer for offer in queryset if offer.term_min <= term <= offer.term_max]

        offers = []
        for offer in queryset:
            client_rate_min = float(request.GET.get('rate_min') or offer.rate_min)
            client_rate_max = float(request.GET.get('rate_max') or offer.rate_max)
            interset_min = max(client_rate_min, offer.rate_min)
            interset_max = min(client_rate_max, offer.rate_max)
            if interset_max >= interset_min:
                offer.rate_min = interset_min
                offers.append(offer)
        price = request.GET.get('price')
        deposit = request.GET.get('deposit')
        if price and deposit:
            for offer in queryset:
                monthly_payment = get_payment(price * (1 - deposit / 100),
                                                      offer.rate_min, term * 12)
                response_data = [{**OfferSerializer(offer).data, 'payment': monthly_payment}
                                 for offer in offers]
                print(response_data)
                return Response(response_data)

        response_data = OfferSerializer(queryset, many=True).data
        return Response(response_data)
