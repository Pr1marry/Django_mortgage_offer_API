from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.test import tag
from .models import Offer


@tag('Offer_model')
class OfferTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = [
            {
                'bank_name': 'sberbank1',
                'term_min': 2,
                'term_max': 10,
                'rate_min': 5.0,
                'rate_max': 10.0,
                'payment_min': 12000,
                'payment_max': 13000,
            },
            {
                'bank_name': 'sberbank2',
                'term_min': 3,
                'term_max': 13,
                'rate_min': 4.0,
                'rate_max': 21.0,
                'payment_min': 14000,
                'payment_max': 16000,
            },
            {
                'bank_name': 'sberbank3',
                'term_min': 15,
                'term_max': 25,
                'rate_min': 5.5,
                'rate_max': 11.0,
                'payment_min': 16300,
                'payment_max': 135000,
            },
        ]
        for offer in self.data:
            Offer.objects.create(**offer)

    def test_list_offer(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.data))

    def test_retrieve_offer(self):
        offer = Offer.objects.first()
        url = reverse('offer-detail', args=(offer.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], offer.id)
        url = reverse('offer-detail', args=(1000,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_offer(self):
        data = {
            "bank_name": "sberbank",
            "term_min": 7,
            "term_max": 10,
            "rate_min": 10.0,
            "rate_max": 15.0,
            "payment_min": 2000,
            "payment_max": 2500,
        }
        offers_count = Offer.objects.count()
        url = reverse('offer-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(offers_count + 1, Offer.objects.count())
        del data['bank_name']
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_offer(self):
        offers_count = Offer.objects.count()
        url = reverse('offer-detail', args=(Offer.objects.first().id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(offers_count - 1, Offer.objects.count())

    def test_list_offer_with_filters(self):
        params = {
            "rate_min": 6,
            "rate_max": 12,
            "ordering": "-payment_min"
        }
        base_url = reverse('offer-list')
        test_url_1 = base_url + "?rate_min={rate_min}&rate_max={rate_max}&ordering={ordering}".format(
            rate_min=params['rate_min'], rate_max=params['rate_max'], ordering=params['ordering'])
        response = self.client.get(test_url_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        offers = Offer.objects.filter(rate_min__gte=params['rate_min'], rate_max__lte=params['rate_max'])
        self.assertEqual(offers.count(), len(response.data))
        for db_offer, res_offer in zip(offers, response.data):
            self.assertEqual(db_offer.id, res_offer['id'])
            self.assertEqual(db_offer.bank_name, res_offer['bank_name'])
