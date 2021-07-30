from django.db import models
from smart_selects.db_fields import ChainedForeignKey


class City(models.Model):
    title = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Street(models.Model):
    title = models.CharField('Название', max_length=100)
    city = models.ForeignKey(City, models.CASCADE, verbose_name='Город')

    def __str__(self):
        return f'{self.city.title} -> {self.title}'

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'


class Shop(models.Model):
    title = models.CharField('Название', max_length=100)
    city = models.ForeignKey(City, models.CASCADE, related_name='cities',
                             verbose_name='Город')
    street = ChainedForeignKey(Street, chained_field='city',
                               chained_model_field='city',
                               related_name='streets', verbose_name='Улица')
    home = models.CharField('Дом', max_length=20)
    opening_time = models.TimeField(verbose_name='Время открытия')
    closing_time = models.TimeField(verbose_name='Время закрытия')

    def __str__(self):
        return f'{self.city.title} -> {self.street.title} -> {self.title}'

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
