from django.db import models


class Offer(models.Model):
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    term_min = models.IntegerField('Срок ипотеки, ОТ', default='10')
    term_max = models.IntegerField('Срок ипотеки, ДО', default='36')
    rate_min = models.FloatField('Ставка, ОТ', default=1.0)
    rate_max = models.FloatField('Ставка, ДО', default=1.0)
    payment_min = models.IntegerField('Сумма кредита, ОТ', default='1000000')
    payment_max = models.IntegerField('Сумма кредита, ДО', default='10000000')

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = 'Ипотечное предложение'
        verbose_name_plural = 'Ипотечные предложения'