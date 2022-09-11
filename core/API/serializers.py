from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

# class OfferSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Offer
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         """Инициализатор сериализатора с зависимостью от типа запроса"""
#         super(OfferSerializer, self).__init__(*args, **kwargs)
#         params = self.context['request'].query_params
#         if self.context['request'].method == 'POST':
#             self.fields['payment'] = serializers.IntegerField(default=None, read_only=True)
#         elif self.context['request'].method == 'PATCH':
#             self.fields['payment'] = serializers.IntegerField(default=0, read_only=True)
#         elif self.context['request'].method == 'GET' and params.get('price') and params.get('term') and params.get('deposit'):
#             self.fields['payment'] = serializers.SerializerMethodField(method_name=calc_payment, read_only=True)
#             self.fields['rate'] = serializers.SerializerMethodField(method_name=calc_rate, read_only=True)
#
#     def calc_rate(self, obj):
#         rate = (obj.rate_min + obj.rate_max) / 2
#         params_dict = self.context['request'].query_params
#         deposit_percent = (int(params_dict.get('deposit')) / int(params_dict.get('price'))) * 100
#         if deposit_percent < 20:
#             rate += 0.2
#         elif deposit_percent > 50:
#             rate -= 0.5
#         return round(rate, 1)
#
#     def calc_payment(self, obj):
#         rate = self.calc_rate(obj)
#         params_dict = self.context['request'].query_params
#         total = round(((int(params_dict.get('price')) - int(params_dict.get('deposit'))) * (rate / 12)) / (
#                     1 - (1 - rate / 12) * (1 - int(params_dict.get('term')) * 12)))
#         return total